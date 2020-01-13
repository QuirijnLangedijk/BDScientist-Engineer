from pyspark.ml.feature import HashingTF, Tokenizer
from pyspark.ml import Pipeline
from pyspark.ml.classification import LinearSVC
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
import time
import src.Part2.frontend.utils.utils as utils


def elapsed_since(start):
    return time.strftime("%H:%M:%S", time.gmtime(time.time() - start))


def train():
    spark = None
    try:
        spark = utils.create_spark()

        print("Just created a SparkContext")
    except ValueError:
        print("SparkContext already exists in this scope")

    if spark:
        start_time = time.time()
        df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
        df = df.drop('_id')
        df.printSchema()
        (train_set, test_set) = df.randomSplit([0.85, 0.15], seed=1234)

        tokenizer = Tokenizer(inputCol="text", outputCol="words")
        hashing_tf = HashingTF(inputCol=tokenizer.getOutputCol(), outputCol="features")
        lsvc = LinearSVC(maxIter=10, regParam=0.1)
        pipeline = Pipeline(stages=[tokenizer, hashing_tf, lsvc])

        param_grid = ParamGridBuilder() \
            .addGrid(hashing_tf .numFeatures, [10, 100, 1000, 10000]) \
            .addGrid(lsvc.regParam, [1, 0.1, 0.01, 0.001]) \
            .build()

        cross_validation = CrossValidator(estimator=pipeline,
                                          estimatorParamMaps=param_grid,
                                          evaluator=BinaryClassificationEvaluator(),
                                          numFolds=3)

        model_cv = cross_validation.fit(train_set)
        evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")

        predictions = model_cv.transform(test_set)
        accuracy = predictions.filter(predictions.label == predictions.prediction).count() / float(test_set.count())
        roc_auc = evaluator.evaluate(predictions)

        print("Accuracy Score: {0:.4f}".format(accuracy))
        print("ROC-AUC: {0:.4f}".format(roc_auc))
        print("Train time:", elapsed_since(start_time))

        pip_model = model_cv.bestModel
        pip_model.write().overwrite().save("./trained/svm.model")
        spark.stop()


train()