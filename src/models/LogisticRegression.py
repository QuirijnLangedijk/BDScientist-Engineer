import re
import nltk
from src.data.get_data import get_all_data
from src.data.process_df import process_df
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from nltk import ConfusionMatrix
from sklearn.metrics import accuracy_score

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