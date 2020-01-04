import warnings

from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
import src.Part2.utils.utils as utils

def train():
    try:
        spark = utils.create_spark()

        print("Just created a SparkContext")
    except ValueError:
        warnings.warn("SparkContext already exists in this scope")

    df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
    df = df.drop('_id')
    df.printSchema()
    (train_set, val_set, test_set) = df.randomSplit([0.80, 0.01, 0.19], seed=1234)

    # Configure an ML pipeline, which consists of three stages: tokenizer, hashingTF, and lr.
    tokenizer = Tokenizer(inputCol="text", outputCol="words")
    hashingTF = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
    lr = LogisticRegression(maxIter=10, regParam=0.001)
    pipeline = Pipeline(stages=[tokenizer, hashingTF, lr])

    model = pipeline.fit(train_set)
    evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")

    predictions = model.transform(val_set)
    accuracy = predictions.filter(predictions.label == predictions.prediction).count() / float(val_set.count())
    roc_auc = evaluator.evaluate(predictions)

    print("Accuracy Score: {0:.4f}".format(accuracy))
    print("ROC-AUC: {0:.4f}".format(roc_auc))

    model.save("./trained/lrm_model.model")
