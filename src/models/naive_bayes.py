import src.data.get_data as gd
from src.data.process_df import process_df
import src.utils.utils as utils

import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from sklearn.metrics import confusion_matrix


def train_nb():
    get_punkt()
    df = gd.get_all_data()
    df = process_df(df)
    pos = []
    neg = []

    for i in range(df.shape[0]-5):
        if i % 1000 == 0:
            print(i)
        neg.append([format_sentence(df.at[i, 'Negative_Review']), 'negative'])
        pos.append([format_sentence(df.at[i, 'Positive_Review']), 'positive'])

    training = pos[:int(.9 * len(pos))] + neg[:int(.9 * len(neg))]
    test = pos[int(.1 * len(pos)):] + neg[int(.1 * len(neg)):]

    classifier = NaiveBayesClassifier.train(training)
    classifier.show_most_informative_features(n=50)

    prediction_result = []
    actual_result = []

    for i in range(len(test)):
        prediction_result.append(classifier.classify(test[i][0]))
        actual_result.append(test[i][1])

    print('\nAccuracy:\n', accuracy(classifier, test))
    print('\nConfusion matrix:\n', confusion_matrix(actual_result, prediction_result))

    utils.save_model('trained_models/naive_bayes/NaiveBayes300k', classifier)


def format_sentence(sentence):
    return {word: True for word in nltk.word_tokenize(sentence)}


def get_punkt():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
