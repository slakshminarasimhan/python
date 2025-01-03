import openai
import streamlit as st
from clickhouse_driver import Client
import json

# Load OpenAI API key
with open('config.json') as f:
    config = json.load(f)
openai.api_key = config['openai_api_key']

# Configure ClickHouse
from clickhouse_driver import Client

# Load ClickHouse credentials
with open('clickhouse_credentials.json') as f:
    clickhouse_credentials = json.load(f)

# Initialize ClickHouse client
client = Client(
    host=clickhouse_credentials['host'],
    port=clickhouse_credentials['port'],
    user=clickhouse_credentials['user'],
    password=clickhouse_credentials['password'],
    database=clickhouse_credentials['database']
)

# Define the ClickHouse schema
schema_description = """
The ClickHouse table `price_volume` contains the following columns:
- `date_time` (Date): The date of the record.
- `security_code` (String): The unique identifier for a stock.
- `open` (Float32): The opening price.
- `high` (Float32): The highest price.
- `low` (Float32): The lowest price.
- `close` (Float32): The closing price.
- `volume` (Int32): The volume of trades.
- `company_name` (String): The name of the company.
- `index_name` (String): The index to which the company belongs.

When searching for a company, use `lower(company_name) LIKE 'company%'` `and index_name = 'Nifty Total Market'`to match partial names, ensuring the query is case-insensitive and supports partial matching.
"""


# Define the OpenAI function
functions = [
    {
        "name": "generate_sql_query",
        "description": "Generate an SQL query for the ClickHouse table based on user input.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The SQL query to execute."
                }
            },
            "required": ["query"]
        }
    }
]

# Function to execute a query in ClickHouse
def execute_query(sql_query):
    try:
        # Execute query and fetch results
        results = client.execute(sql_query)
        return results
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("Natural Language to SQL Query App")
st.subheader("Query your ClickHouse database using natural language")

# User input
user_query = st.text_input("Enter your query (e.g., 'Show average close price for December 2012'): ")

if st.button("Run Query"):
    if user_query:
        # Use OpenAI to convert NL query to SQL
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a SQL expert working with a ClickHouse database."},
                {"role": "system", "content": schema_description},
                {"role": "user", "content": user_query}
            ],
            functions=functions,
            function_call={"name": "generate_sql_query"}
        )

        # Parse the generated query
        sql_query = json.loads(response["choices"][0]["message"]["function_call"]["arguments"])["query"]
        st.code(sql_query, language="sql")

        # Check if the query includes `lower(company_name) LIKE`
        if "lower(company_name) LIKE" not in sql_query:
            st.error("The query did not use the expected filter on company_name.")
        else:
            # Define the function to adjust the query
            def adjust_query(sql_query):
                if "WHERE security_code" in sql_query:
                    sql_query = sql_query.replace("WHERE security_code", "WHERE lower(company_name) LIKE and index_name = 'Nifty Total Market")
                    sql_query = sql_query.replace("=", "LIKE")
                return sql_query

            # Adjust the query
            sql_query = adjust_query(sql_query)

            # Execute the query
            results = execute_query(sql_query)

            if isinstance(results, list) and len(results) > 0:
                # Display query results
                st.write("Query Results:")

                # Dynamically get column names (if needed)
                table_name = sql_query.split("FROM")[1].split(" ")[1].strip()
                column_names = [desc[0] for desc in client.execute(f"DESCRIBE TABLE {table_name}")]
                st.dataframe([dict(zip(column_names, row)) for row in results])
            else:
                st.write("No results or error occurred:", results)
    else:
        st.error("Please enter a query!")
