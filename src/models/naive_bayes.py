import src.data.get_data as gd
from src.data.process_df import process_df
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from sklearn.metrics import confusion_matrix
import pickle
import pandas as pd

test = []


def train_nltk_nb():
    get_punkt()
    df = gd.get_local_dataset()
    df = process_df(df)
    pd.set_option('display.max_columns', None)
    print(df)
    pos = []
    neg = []

    for i in range(100000):
        if i % 1000 == 0:
            print(i)
        neg.append([format_sentence(df.at[i, 'Negative_Review']), 'neg'])
        pos.append([format_sentence(df.at[i, 'Positive_Review']), 'pos'])

    training = pos[:int(.9 * len(pos))] + neg[:int(.9 * len(neg))]
    test = pos[int(.1 * len(pos)):] + neg[int(.1 * len(neg)):]

    classifier = NaiveBayesClassifier.train(training)
    print(accuracy(classifier, test))
    # classifier.show_most_informative_features()

    prediction_result = []
    actual_result = []

    for i in range(len(test)):
        # print(str(test[i][0]) + ' - ' + classifier.classify(test[i][0]))
        prediction_result.append(classifier.classify(test[i][0]))
        actual_result.append(test[i][1])

    print(accuracy(classifier, test))
    print('\nConfusion matrix:\n', confusion_matrix(actual_result, prediction_result))

    save_model('trained_models/naive_bayes/NaiveBayes', classifier)


def classify_nltk_nb(test_line='Wow! I love this hotel, 10/10 would stay again'):
    get_punkt()
    classifier = load_model('trained_models/naive_bayes/NaiveBayes')
    print(classifier.classify(format_sentence(test_line)))


def save_model(name, classifier):
    f = open(name + '.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


def load_model(name):
    f = open(name + '.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


def format_sentence(sentence):
    return {word: True for word in nltk.word_tokenize(sentence)}


def get_punkt():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        nltk.download('punkt')


# train_nltk_nb()
# classify_nltk_nb('very very bad hotel')


