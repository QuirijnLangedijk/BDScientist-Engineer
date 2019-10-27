from sklearn import svm
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk import ConfusionMatrix
import time


import src.data.get_data as gd
import src.utils.utils as utils
from src.data.process_df import process_df


def train_svm():
    df = gd.get_all_data()
    df = process_df(df)

    training_text, training_labels, test_text, test_labels = utils.divide_train_test(df, .8)

    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True,
                                 stop_words="english",
                                 ngram_range=(1, 2))

    train_vectors = vectorizer.fit_transform(training_text)
    test_vectors = vectorizer.transform(test_text)

    classifier = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier.fit(train_vectors, training_labels)
    t1 = time.time()
    predictions = classifier.predict(test_vectors)
    t2 = time.time()

    print("Training time: %fs; Prediction time: %fs" % (t1 - t0, t2 - t1))
    report = classification_report(test_labels, predictions, output_dict=True)
    print('positive: ', report['positive'])
    print('negative: ', report['negative'])

    print('Confusion Matrix:\n', confusion_matrix(test_labels, predictions))
    print(classification_report(test_labels, predictions))
    print(ConfusionMatrix(list(test_labels), list(predictions)))
    print(accuracy_score(test_labels, predictions))

    # utils.save_model('trained_models/svm/vectorizer300k', vectorizer)
    # utils.save_model('trained_models/svm/classifier300k', classifier)
