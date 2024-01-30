import spacy
from spacy.training import Example


# Load the base model
nlp = spacy.load("en_core_web_lg")

# Define the new entity label
ORGLABEL = "ORG"
PERLABEL = "PERSON"

# Prepare training examples
TRAIN_DATA = [
    ("Musk, the CEO of Tesla, is a pioneer in electric cars.", {"entities": [(17, 22, ORGLABEL), (0, 4, PERLABEL)]}),
    ("Musk owns Tesla that makes electric cars.", {"entities": [(10, 15, ORGLABEL),(0, 4, PERLABEL)]}),
    ("Tesla makes electric cars.", {"entities": [(0, 5, ORGLABEL)]}),
    ("Musk is the CEO of Tesla", {"entities": [(19, 24, ORGLABEL),(0, 4, PERLABEL)]}),
    # ... more examples ...
]

# Add the new entity label to the model's pipeline
ner = nlp.get_pipe("ner")
ner.add_label(ORGLABEL)
ner.add_label(PERLABEL)

# Update the model with the training examples
optimizer = nlp.resume_training()
for text, annotations in TRAIN_DATA:
    doc = nlp.make_doc(text)
    example = Example.from_dict(doc, annotations)
     # Correctly define `losses` within the loop
    losses = {}  # Initialize empty dictionary for losses
    nlp.update([example], drop=0.5, losses=losses, sgd=optimizer)

# Save the trained model
nlp.to_disk("custom_ner_model")


# Tesla makes electric cars - ORG=Tesla
# Musk is the owner of Tesla - ORG=Tesla, PERSON=Musk
# Musk makes electric cars - PERSON=Musk, here i want ORG to be ORG=Tesla
# How do i train ?