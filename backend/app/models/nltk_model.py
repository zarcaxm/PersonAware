""" import nltk
import pickle

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

with open('nltk_classifier.pkl', 'rb') as f:
    nltk_classifier = pickle.load(f)


def word_features(word):
    return {"word": word, "is_capitalized": word[0].isupper()}


def process_with_nltk(text_content):
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
 """
