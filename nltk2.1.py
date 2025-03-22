import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

# Load the train.csv data
train_df = pd.read_csv("https://raw.githubusercontent.com/PolyAI-LDN/task-specific-datasets/master/banking_data/train.csv")

# Initialize TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the 'text' column
train_vectors = vectorizer.fit_transform(train_df['text'])

# Create a DataFrame to store the concepts
concept_df = train_df.copy()

# Add concept vectors as a new column (storing as lists)
concept_df['concept_vector'] = list(train_vectors.toarray().tolist()) #added .tolist() here.

# Save the DataFrame to a local CSV file
concept_df.to_csv("output/train_with_concepts.csv", index=False)

print("train_with_concepts.csv created successfully!")

# #load the newly created csv.
# concept_df = pd.read_csv("output/train_with_concepts.csv")

# def get_answer(question):
#     """Answers questions using concept_vector similarity."""
#     question_vector = vectorizer.transform([question])

#     similarities = []
#     for concept_vector_str in concept_df['concept_vector']:
#         # Convert the string representation of the list back to a list
#         concept_vector = eval(concept_vector_str)
#         similarities.append(cosine_similarity(question_vector, [concept_vector])[0][0])

#     most_similar_index = similarities.index(max(similarities))

#     if similarities[most_similar_index] > 0.2: # simple threshold.
#         return concept_df['category'][most_similar_index]
#     else:
#         return "I'm sorry, I couldn't find a relevant answer."

# def chat_concepts_bot():
#     """Chatbot using concept_vector from train_with_concepts.csv."""
#     print("Welcome to the Banking Concept Chatbot!")
#     while True:
#         question = input("You: ")
#         if question.lower() == "quit":
#             break
#         answer = get_answer(question)
#         print("Bot:", answer)

# chat_concepts_bot()