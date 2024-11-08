import spacy
import re

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined list of financial and data-related keywords
financial_keywords = {
    "stock", "data", "analyze", "RSI", "MACD", "SMA", "rolling", "EMA",
    "time series", "plot", "date", "start date", "window", "scalar", "PNG", "error",
    "close", "closing", "open", "high", "low", "price", "volume"
}

def extract_domain_keywords(text):
    # Process text with spaCy
    doc = nlp(text)

    # Extract financial keywords from text by directly searching the text
    # Use case-insensitive search by converting both to lowercase
    extracted_keywords = {word for word in financial_keywords if re.search(r'\b' + re.escape(word) + r'\b', text, re.IGNORECASE)}
    
    # Additionally, check if any entities match the financial_keywords
    entities = {ent.text.lower() for ent in doc.ents}
    matched_entities = entities & financial_keywords
    
    # Combine extracted keywords from direct search and entities
    final_keywords = extracted_keywords | matched_entities
    
    return list(final_keywords)

# Sample complex input
text = """Give me a list of stocks where closing price is above 1000 and RSI was above 60 and MACD is above 50 and volume more than 200000."""

# Extract keywords for querying
domain_keywords = extract_domain_keywords(text)
print("Financial & Data Keywords for Database Query:", domain_keywords)
