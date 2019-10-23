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
