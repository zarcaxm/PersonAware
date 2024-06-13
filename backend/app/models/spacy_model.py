import spacy
import os

# Get the absolute path to the directory containing this file
models_dir = os.path.dirname(__file__)

# Construct the full path to the spaCy model directory
spacy_model_path = os.path.join(models_dir, "spacyM1")

# Load the spaCy model
spacy_nlp = spacy.load(spacy_model_path)


def process_with_spacy(text_content):
    doc = spacy_nlp(text_content)
    return [(ent.text, ent.label_) for ent in doc.ents]
