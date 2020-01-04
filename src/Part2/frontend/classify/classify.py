import utils.utils as utils
from pyspark.ml import PipelineModel


def classify_lr(sentence):
    try:
        spark = utils.create_spark()
        model = PipelineModel.load("models/trained/lrm_model.model")

        test = spark.createDataFrame([
            (4, sentence)
        ], ["id", "text"])

        prediction = model.transform(test)
        selected = prediction.select("id", "text", "probability", "prediction")
        for row in selected.collect():
            rid, text, prob, _prediction = row
            if _prediction == 0.000000:
                return "Review: %s is a: %s review. The model is %f%% sure." % (text, 'negative', prob[0]*100)
            else:
                return "Review: %s is a: %s review.  The model is %f%% sure." % (text, 'positive', prob[1]*100)

    except ValueError:
        print('error')


