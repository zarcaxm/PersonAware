""" from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

hft_model_path = 'bert-model'
hft_tokenizer = AutoTokenizer.from_pretrained(hft_model_path)
hft_model = AutoModelForTokenClassification.from_pretrained(hft_model_path)
hft_pipeline = pipeline("ner", model=hft_model, tokenizer=hft_tokenizer)


def process_with_hft(text_content):
    ner_results = hft_pipeline(text_content)
    entities = [{"text": result['word'], "label": result['entity'],
                 "score": result['score']} for result in ner_results]
    return entities
 """
