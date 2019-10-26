import pickle


def save_model(name, classifier):
    f = open(name + '.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


def load_model(name):
    f = open(name + '.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()
    return classifier


def divide_train_test(df, ratio_train=.8):
    text_pos = []
    labels_pos = []
    text_neg = []
    labels_neg = []

    for i in range(df.shape[0]-5000):
    # for i in range(100000):
        if i % 10000 == 0:
            print(i)
        text_pos.append(df.at[i, 'Positive_Review'].lower())
        labels_pos.append('positive')
        text_neg.append(df.at[i, 'Negative_Review'].lower())
        labels_neg.append('negative')

    training_text = text_pos[:int(ratio_train*len(text_pos))] + text_neg[:int(ratio_train*len(text_neg))]
    training_labels = labels_pos[:int(ratio_train*len(labels_pos))] + labels_neg[:int(ratio_train*len(labels_neg))]

    test_text = text_pos[int(ratio_train*len(text_pos)):] + text_neg[int(ratio_train*len(text_neg)):]
    test_labels = labels_pos[int(ratio_train*len(labels_pos)):] + labels_neg[int(ratio_train*len(labels_neg)):]

    return [training_text, training_labels, test_text, test_labels]
