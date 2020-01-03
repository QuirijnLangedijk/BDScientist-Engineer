import src.Part2.utils.utils as utils
from simple_colors import *
from pyspark.ml import PipelineModel


def classify():
    try:
        spark = utils.create_spark()
        model = PipelineModel.load("../models/trained/lrm_model.model")

        test = spark.createDataFrame([
            (4, "Such a bad hotel, Im never coming back"),
            (5, "Very good hotel, Would stay here again"),
            (6, "I was going to give a positive review, however, the shower broke halfway through our trip ,ruining our vacation"),
            (7, "This hotel was lovely")
        ], ["id", "text"])

        prediction = model.transform(test)
        selected = prediction.select("id", "text", "probability", "prediction")
        for row in selected.collect():
            rid, text, prob, _prediction = row
            if _prediction == 0.000000:
                print("Review: %s is a: %s review. The model is %f%% sure." % (text, red('negative', 'bold'), prob[0]*100))
            else:
                print("Review: %s is a: %s review. The model is %f%% sure." % (text, green('positive', 'bold'), prob[1]*100))

    except ValueError:
        print('error')


classify()