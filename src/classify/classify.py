from src.models.naive_bayes import get_punkt, format_sentence, train_nb
from src.models.svm import train_svm
from src.models.logistic_regression import train_lr
import src.utils.utils as utils


def classify_sentences_svm(sentences):
    vectorizer = utils.load_model('../models/trained_models/svm/vectorizer300k')
    classifier = utils.load_model('../models/trained_models/svm/classifier300k')

    print('Support Vector Machine: ')
    for sentence in sentences:
        review_vector = vectorizer.transform([sentence])
        print(classifier.predict(review_vector)[0] + ': ' + sentence)


def classify_nb(sentences):
    get_punkt()
    classifier = utils.load_model('../models/trained_models/naive_bayes/NaiveBayes300k')

    print('\nNaive Bayes: ')
    for sentence in sentences:
        print(classifier.classify(format_sentence(sentence)) + ': ' + sentence)


def classify_lg(sentences):
    vectorizer = utils.load_model('../models/trained_models/logistic_regression/vectorizer300k')
    classifier = utils.load_model('../models/trained_models/logistic_regression/classifier300k')

    print('\nLogistic Regression: ')
    for sentence in sentences:
        review_vector = vectorizer.transform([sentence])
        print(classifier.predict(review_vector)[0] + ': ' + sentence)


def classify_all():
    sentences = [
        'This hotel was great! I would recommend staying here',
        'I didn\'t like this hotel at all, Im not coming back',
        'The shower was broken'
    ]
    classify_sentences_svm(sentences)
    classify_nb(sentences)
    classify_lg(sentences)


def train_all():
    train_nb()
    train_svm()
    train_lr()


classify_all()
