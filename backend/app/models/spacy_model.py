import spacy
import os

models_dir = os.path.dirname(__file__)

spacy_model_path = os.path.join(models_dir, "spacyM1")

if not os.path.exists(spacy_model_path):
    raise FileNotFoundError(
        f"A diretoria para o modelo '{spacy_model_path}' não existe. Por favor tente outra libraria")

try:
    spacy_nlp = spacy.load(spacy_model_path)
except Exception as e:
    raise RuntimeError(
        f"Falha ao carregar modelo '{spacy_model_path}': {e}")


def process_with_spacy(text_content):
    doc = spacy_nlp(text_content)
    return [(ent.text, ent.label_) for ent in doc.ents]
