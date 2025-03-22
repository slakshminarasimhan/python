import pandas as pd
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from annoy import AnnoyIndex
import numpy as np

nltk.download('punkt', quiet=True)

try:
    concept_df = pd.read_csv("output/train_with_concepts.csv")
    vectorizer = TfidfVectorizer()
    vectorizer.fit(concept_df['text'])

    # Build Annoy index
    f = len(eval(concept_df['concept_vector'][0]))  # Vector dimensionality
    t = AnnoyIndex(f, 'angular')  # Angular distance is equivalent to cosine similarity
    for i, concept_vector_str in enumerate(concept_df['concept_vector']):
        concept_vector = eval(concept_vector_str)
        t.add_item(i, concept_vector)
    t.build(10)  # 10 trees

except FileNotFoundError:
    print("train_with_concepts.csv not found. Please run the data processing script first.")
    exit()

def get_top_n_matches_annoy(question, n=5):
    """Returns the top n matching categories using Annoy."""
    question_vector = vectorizer.transform([question]).toarray()[0]
    nearest_indices = t.get_nns_by_vector(question_vector, n)
    results = [(cosine_similarity([question_vector], [eval(concept_df['concept_vector'][i])])[0][0], concept_df['category'][i]) for i in nearest_indices]
    return results

def chat_concepts_bot():
    """Chatbot using Annoy for faster similarity search."""
    print("Welcome to the Banking Concept Chatbot!")
    print("Enter 99 to exit.")
    while True:
        question = input("You: ")
        if question.lower() == "99":
            break

        matches = get_top_n_matches_annoy(question)

        if matches:
            print("Top matching categories:")
            for i, (similarity, category) in enumerate(matches):
                print(f"{i + 1}. {category} (Similarity: {similarity:.4f})")

            choice = input("Enter the number of the category you're interested in (or 0 for none): ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(matches):
                    category = matches[choice - 1][1]
                    print(f"You selected: {category}")
                    print("Retrieving information...")
                elif choice == 0:
                    print("Okay.")
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")

        else:
            print("I'm sorry, I couldn't find a relevant answer.")

chat_concepts_bot()