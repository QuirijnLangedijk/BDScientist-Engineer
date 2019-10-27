from src.models.naive_bayes import get_punkt, format_sentence, train_nb
from src.models.svm import train_svm
from src.models.logistic_regression import train_lr
from prettytable import PrettyTable
import time
import emoji

import src.utils.utils as utils


def classify_sentences_svm():
    vectorizer = utils.load_model('../models/trained_models/svm/vectorizer300k')
    classifier = utils.load_model('../models/trained_models/svm/classifier300k')

    classified = []
    for sentence in sentences:
        review_vector = vectorizer.transform([sentence])
        classified.append([classifier.predict(review_vector)[0], sentence])
    return classified


def classify_nb():
    get_punkt()
    classifier = utils.load_model('../models/trained_models/naive_bayes/NaiveBayes')

    classified = []
    for sentence in sentences:
        classified.append([classifier.classify(format_sentence(sentence)), sentence])
    return classified


def classify_lg():
    vectorizer = utils.load_model('../models/trained_models/logistic_regression/vectorizer100k')
    classifier = utils.load_model('../models/trained_models/logistic_regression/classifier100k')

    classified = []
    for sentence in sentences:
        review_vector = vectorizer.transform([sentence])
        classified.append([classifier.predict(review_vector)[0], sentence])
    return classified


def classify_all_with_check():
    t0 = time.time()
    classified = [classify_sentences_svm(), classify_nb(), classify_lg()]
    t1 = time.time()
    print('time:', round(float(t1 - t0), 2), ' seconds')
    t = PrettyTable(['Classified As', 'Model', 'Sentence', 'Correct?'])
    for i in range(len(sentences)):
        # Support Vector Machine
        if classified[0][i][0] == validation[i]:
            t.add_row([classified[0][i][0], 'Support Vector Machine', classified[0][i][1],
                       emoji.emojize(':white_check_mark:', use_aliases=True)])
        else:
            t.add_row([classified[0][i][0], 'Support Vector Machine', classified[0][i][1],
                       emoji.emojize(':x:', use_aliases=True)])

        # Naive Bayes
        if classified[1][i][0] == validation[i]:
            t.add_row([classified[1][i][0], 'Naive Bayes', classified[1][i][1],
                       emoji.emojize(':white_check_mark:', use_aliases=True)])
        else:
            t.add_row([classified[1][i][0], 'Naive Bayes', classified[1][i][1],
                       emoji.emojize(':x:', use_aliases=True)])

        # Logistic Regression
        if classified[2][i][0] == validation[i]:
            t.add_row([classified[2][i][0], 'Logistic Regression', classified[2][i][1],
                       emoji.emojize(':white_check_mark:', use_aliases=True)])
        else:
            t.add_row([classified[2][i][0], 'Logistic Regression', classified[2][i][1],
                       emoji.emojize(':x:', use_aliases=True)])

        if i != len(sentences) - 1:
            t.add_row(['---', '---', '---', '---'])
    print(t)


def classify_all():
    t0 = time.time()
    classified = [classify_sentences_svm(), classify_nb(), classify_lg()]
    t1 = time.time()
    print('time:', round(float(t1 - t0), 2), ' seconds')
    t = PrettyTable(['Classified As', 'Model', 'Sentence'])
    for i in range(len(sentences)):
        t.add_row([classified[0][i][0], 'Support Vector Machine', classified[0][i][1]])
        t.add_row([classified[1][i][0], 'Naive Bayes', classified[1][i][1]])
        t.add_row([classified[2][i][0], 'Logistic Regression', classified[2][i][1]])
        if i != len(sentences) - 1:
            t.add_row(['-', '-', '- '])
    print(t)


def train_all():
    train_nb()
    train_svm()
    train_lr()


sentences = [
    'This hotel is really good',
    'The shower was broken and we werent compensated for it',
    'I want my money back',
    'This hotel was great! I would recommend staying here',
    'I didn\'t like this hotel at all, Im not coming back',
    'Great hotel'
]

validation = [
    'pos',
    'neg',
    'neg',
    'pos',
    'neg',
    'pos'
]

classify_all_with_check()
classify_all()