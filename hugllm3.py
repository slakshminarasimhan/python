from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, AutoModelForTokenClassification

# Assuming your existing model setups
tokenizer_gpt2 = AutoTokenizer.from_pretrained("gpt2")
model_gpt2 = AutoModelForCausalLM.from_pretrained("gpt2")
nlp_generation = pipeline("text-generation", model=model_gpt2, tokenizer=tokenizer_gpt2)

tokenizer_ner = AutoTokenizer.from_pretrained("dslim/bert-base-NER")
model_ner = AutoModelForTokenClassification.from_pretrained("dslim/bert-base-NER")
nlp_ner = pipeline("ner", model=model_ner, tokenizer=tokenizer_ner)

#example = "My name is Wolfgang and I live in Berlin. I work at ABC Corporation and enjoy spending time at XYZ Company."

example = "Adani Exports Limited started as a commodity trading company in 1988 and expanded \
    into importing and exporting multiple commodities. With a capital of ₹5 lakhs, the company was \
        established as a partnership firm with the flagship company Adani Enterprises, previously \
            Adani Exports.[23] In 1990, the Adani Group developed its own port in Mundra to provide a base \
                for its trading operations. It began construction at Mundra in 1995. In 1998, it became the top net \
                    foreign exchange earner for India Inc.[24] The company began coal trading in 1999, \
                        followed by a joint venture in edible oil refining in 2000 with the formation of \
                            Adani Wilmar.[25]"

# Generate text
generated_text = nlp_generation(example, max_length=100, num_return_sequences=1)[0]['generated_text']

print("Generated Text:")
print(generated_text)

# Extract entities from generated text and reconstruct full names
ner_results = nlp_ner(generated_text)
print("\nExtracted Entities:")

print("\nUnique Entities:")
unique_labels = set(entity['entity'] for entity in ner_results)
print(unique_labels)


current_entity = ''
full_entities = []
for entity in ner_results:
    if entity['entity'].startswith('B-'):  # Start of a new entity
        if current_entity:
            full_entities.append(current_entity.strip())  # Append the previous entity
        current_entity = entity['word']
    elif entity['entity'].startswith('I-'):  # Inside an entity
        current_entity += entity['word'].replace('##', '')
if current_entity:  # Append the last entity
    full_entities.append(current_entity.strip())

print("\nFull Entity Names:")
print(full_entities)
