import src.Part1.data.get_data as gd
from src.Part1.data.process_df import process_df

import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from sklearn.metrics import confusion_matrix
import contractions
import string


TR_TE_SPLIT = .8


def train_nb():
    get_punkt()
    df = gd.get_all_data()
    df = process_df(df)
    pos = []
    neg = []

    # -5 for out of range bugfix
    for i in range(df.shape[0]-5):
        # To lowercase and remove punctuation in order to improve accuracy
        neg.append([format_sentence(df.at[i, 'Negative_Review'].lower().translate(None, string.punctuation)), 'negative'])
        pos.append([format_sentence(df.at[i, 'Positive_Review'].lower().translate(None, string.punctuation)), 'positive'])

    X = pos[:int(TR_TE_SPLIT * len(pos))] + neg[:int(TR_TE_SPLIT * len(neg))]
    y = pos[int(TR_TE_SPLIT * len(pos)):] + neg[int(TR_TE_SPLIT * len(neg)):]

    classifier = NaiveBayesClassifier.train(X)

    prediction_result = []
    actual_result = []

    for i in range(len(y)):
        prediction_result.append(classifier.classify(y[i][0]))
        actual_result.append(y[i][1])

    classifier.show_most_informative_features(n=50)
    print('\nAccuracy:\n', accuracy(classifier, y))
    print('\nConfusion matrix:\n', confusion_matrix(actual_result, prediction_result))

    # utils.save_model('trained_models/naive_bayes/NaiveBayes300k', classifier)


def format_sentence(sentence):
    # Changes words like can't to can not and ya'll to you all
    sentence = contractions.fix(sentence, slang=True)
    return {word: True for word in nltk.word_tokenize(sentence)}


def get_punkt():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')
