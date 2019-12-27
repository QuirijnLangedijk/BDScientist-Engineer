from nltk import ConfusionMatrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.feature_extraction.text import TfidfVectorizer
import time

import src.Part1.data.get_data as gd
import src.Part1.utils.utils as utils
from src.Part1.data.process_df import process_df

TRAIN_SIZE = .8


def train_lr():
    df = gd.get_all_data()
    df = process_df(df)

    training_text, training_labels, test_text, test_labels = utils.divide_train_test(df, TRAIN_SIZE)

    vectorizer = TfidfVectorizer(min_df=25,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)

    train_vectors = vectorizer.fit_transform(training_text)
    test_vectors = vectorizer.transform(test_text)

    classifier = LogisticRegression()
    t0 = time.time()
    classifier.fit(train_vectors, training_labels)
    t1 = time.time()
    predictions = classifier.predict(test_vectors)
    t2 = time.time()

    print("Training time: %fs; Prediction time: %fs" % (t1 - t0, t2 - t1))
    report = classification_report(test_labels, predictions, output_dict=True)
    print('positive: ', report['positive'])
    print('negative: ', report['negative'])

    print(classification_report(test_labels, predictions))
    print(ConfusionMatrix(list(test_labels), list(predictions)))
    print(accuracy_score(test_labels, predictions))

    #utils.save_model('trained_models/logistic_regression/vectorizer300k', vectorizer)
    #utils.save_model('trained_models/logistic_regression/classifier300k', classifier)
