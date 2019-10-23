from nltk import ConfusionMatrix
from sklearn.metrics import accuracy_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

import src.data.get_data as gd
import src.utils.utils as utils
from src.data.process_df import process_df


def train_lr():
    df = gd.get_local_dataset()
    df = process_df(df)

    text_pos = []
    labels_pos = []
    text_neg = []
    labels_neg = []

    for i in range(100000):
        text_pos.append(df.at[i, 'Positive_Review'])
        labels_pos.append('pos')
        text_neg.append(df.at[i, 'Negative_Review'])
        labels_neg.append('neg')

    training_text = text_pos[:int((.8)*len(text_pos))] + text_neg[:int((.8)*len(text_neg))]
    training_labels = labels_pos[:int((.8)*len(labels_pos))] + labels_neg[:int((.8)*len(labels_neg))]

    test_text = text_pos[int((.8)*len(text_pos)):] + text_neg[int((.8)*len(text_neg)):]
    test_labels = labels_pos[int((.8)*len(labels_pos)):] + labels_neg[int((.8)*len(labels_neg)):]

    vectorizer = CountVectorizer(
        analyzer='word',
        lowercase=False,
        max_features=100
    )

    features = vectorizer.fit_transform(
        training_text + test_text)

    features_nd = features.toarray()

    x_train, x_test, y_train, y_test = train_test_split(
        features_nd[0:len(training_text)],
        training_labels,
        train_size=0.80,
        random_state=1234)

    logmodel = LogisticRegression()
    logmodel.fit(x_train, y_train)
    predictions = logmodel.predict(x_test)
    print(classification_report(y_test, predictions))
    print(ConfusionMatrix(list(y_test), list(predictions)))
    print(accuracy_score(y_test, predictions))

    utils.save_model('trained_models/logistic_regression/vectorizer', vectorizer)
    utils.save_model('trained_models/logistic_regression/classifier', logmodel)
