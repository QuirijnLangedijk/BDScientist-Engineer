import re
import nltk
from src.data.get_data import get_all_data
from src.data.process_df import process_df
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from nltk import ConfusionMatrix
from sklearn.metrics import accuracy_score
import nltk
from nltk.classify import NaiveBayesClassifier
from nltk.classify.util import accuracy
from sklearn.metrics import confusion_matrix
import pickle

test = []


def sklearn_regression():
    df = get_all_data()
    df = process_df(df)
    neg_list = list(df['Negative_Review'])
    pos_list = list(df['Positive_Review'])

    training_reviews = pos_list[:int((.1) * len(pos_list))] + neg_list[:int((.1) * len(neg_list))]
    training_labels = ['pos']*(int((.1) * len(pos_list))) + ['neg']*(int((.1) * len(neg_list)))

    test_reviews = pos_list[int((.9) * len(pos_list)):] + neg_list[int((.9) * len(neg_list)):]
    test_labels = ['pos']*(int((.1) * len(pos_list))) + ['neg']*(int((.1) * len(neg_list)))
    print(len(training_reviews))
    print(len(training_labels))

    vectorizer = CountVectorizer(
        analyzer='word',
        lowercase=False,
        max_features=100
    )

    features = vectorizer.fit_transform(
        training_reviews + test_reviews)
    features_nd = features.toarray()

    X_train, X_test, y_train, y_test = train_test_split(
            features_nd[0:len(training_reviews)],
            training_labels,
            train_size=0.80,
            random_state=1234)

    log_model = LogisticRegression()
    log_model = log_model.fit(X=X_train, y=y_train)
    y_pred = log_model.predict(X_test)

    print('Confusion Matrix:')
    print(ConfusionMatrix(list(y_test), list(y_pred)))

    print('Accuracy score: ')
    print(accuracy_score(y_test, y_pred))


def train_nltk_regression():
    nltk.download('punkt')
    df = get_all_data()
    df = process_df(df)
    pos = []
    neg = []

    for i in range(100000):
        if i % 1000 == 0: print(i)
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

    save_model('NaiveBayes', classifier)


def classify_nltk_regression(test_line='Wow! I love this hotel, 10/10 would stay again'):
    nltk.download('punkt')
    classifier = load_model('NaiveBayes')
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
    return({word: True for word in nltk.word_tokenize(sentence)})


# classify_nltk_regression('This hotel great')

