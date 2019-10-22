from sklearn.feature_extraction.text import TfidfVectorizer
import pickle
import time
from sklearn import svm
from sklearn.metrics import classification_report

import src.data.get_data as gd
from src.data.process_df import process_df


def train_svm():
    df = gd.get_local_dataset()
    df = process_df(df)

    text_pos = []
    labels_pos = []
    text_neg = []
    labels_neg = []

    for i in range(df.shape[0]):
        text_pos.append(df.at[i, 'Positive_Review'])
        labels_pos.append('pos')
        text_neg.append(df.at[i, 'Negative_Review'])
        labels_neg.append('neg')

    training_text = text_pos[:int((.8)*len(text_pos))] + text_neg[:int((.8)*len(text_neg))]
    training_labels = labels_pos[:int((.8)*len(labels_pos))] + labels_neg[:int((.8)*len(labels_neg))]

    test_text = text_pos[int((.8)*len(text_pos)):] + text_neg[int((.8)*len(text_neg)):]
    test_labels = labels_pos[int((.8)*len(labels_pos)):] + labels_neg[int((.8)*len(labels_neg)):]

    vectorizer = TfidfVectorizer(min_df=5,
                                 max_df=0.8,
                                 sublinear_tf=True,
                                 use_idf=True)

    train_vectors = vectorizer.fit_transform(training_text)
    test_vectors = vectorizer.transform(test_text)

    # Perform classification with SVM, kernel=linear
    classifier_linear = svm.SVC(kernel='linear')
    t0 = time.time()
    classifier_linear.fit(train_vectors, training_labels)
    t1 = time.time()
    prediction_linear = classifier_linear.predict(test_vectors)
    t2 = time.time()
    time_linear_train = t1 - t0
    time_linear_predict = t2 - t1
    # results
    print("Training time: %fs; Prediction time: %fs" % (time_linear_train, time_linear_predict))
    report = classification_report(test_labels, prediction_linear, output_dict=True)
    print('positive: ', report['pos'])
    print('negative: ', report['neg'])

    save_model('trained_models/svm/vectorizer', vectorizer)
    save_model('trained_models/svm/classifier', classifier_linear)


def save_model(name, classifier):
    f = open(name + '.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


def load_model(name):
    f = open(name + '.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


def classify_sentences(sentences):
    vectorizer = load_model('trained_models/svm/vectorizer')
    classifier = load_model('trained_models/svm/classifier')

    for sentence in sentences:
        review_vector = vectorizer.transform([sentence])
        print(classifier.predict(review_vector))


# train_svm()
# classify_sentences(['very good hotel', 'very bad hotel', 'awful hotel'])
