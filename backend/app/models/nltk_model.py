import nltk
import pickle
import os


def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        nltk.download('averaged_perceptron_tagger')


download_nltk_data()

nltk_classifier = None
classifier_path = 'nltk_classifier.pkl'

if os.path.exists(classifier_path):
    try:
        with open(classifier_path, 'rb') as f:
            nltk_classifier = pickle.load(f)
    except Exception as e:
        print(f"Failed to load NLTK classifier from '{classifier_path}' : {e}")
else:
    print(f"The NLTK classifier file '{classifier_path}' does not exist. ")


def word_features(word):
    return {"word": word, "is_capitalized": word[0].isupper()}


def process_with_nltk(text_content):
    if nltk_classifier is None:
        raise ValueError("The NLTK classifier is not available.")

    tokens = nltk.word_tokenize(text_content)
    classified_tokens = [
        (token, nltk_classifier.classify(word_features(token))) for token in tokens]

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
