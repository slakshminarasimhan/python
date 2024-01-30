import spacy
# Load the custom NER model
nlp = spacy.load("custom_ner_model")

text = "Tesla makes electric cars"
doc = nlp(text)

print("Entities:", [(ent.text, ent.label_) for ent in doc.ents])
