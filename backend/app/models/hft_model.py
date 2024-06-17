from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import os

hft_model_path = ''


def load_huggingface_model(model_path):
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        model = AutoModelForTokenClassification.from_pretrained(model_path)
        return pipeline("ner", model=model, tokenizer=tokenizer)
    except Exception as e:
        raise RuntimeError(
            f"Failed to load Hugging Face Transformers model from '{model_path}': {e}")


try:
    if os.path.exists(hft_model_path):
        hft_pipeline = load_huggingface_model(hft_model_path)
    else:
        hft_pipeline = load_huggingface_model('')
except Exception as e:
    print(e)
    hft_pipeline = None


def process_with_hft(text_content):
    if hft_pipeline is None:
        raise ValueError(
            "The Hugging Face Transformers model is not available.")

    ner_results = hft_pipeline(text_content)
    entities = [{"text": result['word'], "label": result['entity'],
                 "score": result['score']} for result in ner_results]
    return entities
