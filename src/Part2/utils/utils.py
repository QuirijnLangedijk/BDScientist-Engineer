from pyspark.sql import SparkSession
import pickle


def create_spark():
    return SparkSession.builder.appName("myApp") \
            .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/PO2.balanced_data3") \
            .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/PO2.balanced_data3") \
            .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.2') \
            .getOrCreate()


def save_model(name, classifier):
    f = open(name + '.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()


def load_model(name):
    f = open(name + '.pickle', 'rb')
    model = pickle.load(f)
    f.close()
    return model
