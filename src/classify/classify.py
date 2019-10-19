import pickle

from src.models.naive_bayes import get_punkt, format_sentence, train_nltk_nb
from src.models.svm import train_svm


def load_model(name):
    f = open(name + '.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


def classify_sentences_svm(sentences):
    vectorizer = load_model('../models/trained_models/svm/vectorizer')
    classifier = load_model('../models/trained_models/svm/classifier')

    print('SVM: ')
    for sentence in sentences:
        review_vector = vectorizer.transform([sentence])
        print(classifier.predict(review_vector)[0] + ': ' + sentence)


def classify_nltk_nb(sentences):
    get_punkt()

    print('\nNaive Bayes: ')
    for sentence in sentences:
        classifier = load_model('../models/trained_models/naive_bayes/NaiveBayes')
        print(classifier.classify(format_sentence(sentence)) + ': ' + sentence)


def classify_all():
    sentences = [
        'This hotel was great! I would recommend staying here',
        'I didn\'t like this hotel at all, Im not coming back',
        'Great hotel'
    ]
    classify_sentences_svm(sentences)
    classify_nltk_nb(sentences)


def train_all():
    train_nltk_nb()
    train_svm()


classify_all()