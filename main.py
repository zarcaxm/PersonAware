from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
import os
import pypandoc
import spacy
import nltk
import pickle
from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline

try:
    pypandoc.get_pandoc_version()
except OSError:
    pypandoc.download_pandoc()

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

spacy_nlp = spacy.load("spacyM1")

with open('nltk_classifier.pkl', 'rb') as f:
    nltk_classifier = pickle.load(f)

hft_model_path = 'bert-model'
hft_tokenizer = AutoTokenizer.from_pretrained(hft_model_path)
hft_model = AutoModelForTokenClassification.from_pretrained(hft_model_path)
hft_pipeline = pipeline("ner", model=hft_model, tokenizer=hft_tokenizer)

app = FastAPI()


def process_with_spacy(text_content):
    doc = spacy_nlp(text_content)
    return [(ent.text, ent.label_) for ent in doc.ents]


def process_with_nltk(text_content):
    def word_features(word):
        return {"word": word, "is_capitalized": word[0].isupper()}

    tokens = nltk.word_tokenize(text_content)
    classified_tokens = [(token, nltk_classifier.classify(
        word_features(token))) for token in tokens]

    entities = []
    current_entity = []
    for token, label in classified_tokens:
        if label.startswith('B-'):
            if current_entity:
                entities.append(
                    (' '.join([t for _, t in current_entity]), current_entity[0][0]))
                current_entity = []
            current_entity.append((label[2:], token))
        elif label.startswith('I-') and current_entity:
            current_entity.append((label[2:], token))
        else:
            if current_entity:
                entities.append(
                    (' '.join([t for _, t in current_entity]), current_entity[0][0]))
                current_entity = []
    if current_entity:
        entities.append(
            (' '.join([t for _, t in current_entity]), current_entity[0][0]))
    return entities


def process_with_hft(text_content):
    ner_results = hft_pipeline(text_content)
    entities = [{"text": result['word'], "label": result['entity'],
                 "score": result['score']} for result in ner_results]
    return entities


@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...), library: str = Form(...)):
    file_location = f"./{file.filename}"

    with open(file_location, "wb") as f:
        f.write(await file.read())

    output_file_location = file_location.rsplit('.', 1)[0] + '.txt'

    pypandoc.convert_file(file_location, 'plain',
                          outputfile=output_file_location)

    with open(output_file_location, "r", encoding="utf-8") as f:
        text_content = f.read()

    if library == 'spaCy':
        entities = process_with_spacy(text_content)
    elif library == 'NLTK':
        entities = process_with_nltk(text_content)
    elif library == 'HFT':
        entities = process_with_hft(text_content)
    else:
        return {"error": "Invalid library chosen."}

    return {
        "info": f"file '{file.filename}' saved and converted to '{output_file_location}'",
        "entities": entities
    }


@app.get("/")
async def main():
    content = """
    <body>
    <form action="/uploadfile/" enctype="multipart/form-data" method="post">
    <label for="library">Choose a library:</label>
    <select name="library" id="library">
      <option value="spaCy">spaCy</option>
      <option value="NLTK">NLTK</option>
      <option value="HFT">HFT</option>
    </select>
    <input name="file" type="file">
    <input type="submit">
    </form>
    </body>
    """
    return HTMLResponse(content=content)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
