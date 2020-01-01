import findspark
import pyspark as ps
import warnings
from pyspark.sql import SQLContext
from pyspark.sql import SparkSession
from pyspark.ml.feature import HashingTF, IDF, Tokenizer
from pyspark.ml.feature import StringIndexer
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import BinaryClassificationEvaluator
from pyspark.ml.feature import CountVectorizer

from src.Part2.db.db_utils import get_balanced_data

findspark.init()


try:
    spark = SparkSession.builder.appName("myApp") \
        .config("spark.mongodb.input.uri", "mongodb://127.0.0.1/PO2.balanced_data2") \
        .config("spark.mongodb.output.uri", "mongodb://127.0.0.1/PO2.balanced_data2") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.2') \
        .getOrCreate()

    print("Just created a SparkContext")
except ValueError:
    warnings.warn("SparkContext already exists in this scope")

df = spark.read.format("com.mongodb.spark.sql.DefaultSource").load()
df = df.drop('_id')
df.printSchema()

print(df.show(1000))
(train_set, val_set, test_set) = df.randomSplit([0.80, 0.01, 0.19], seed=1234)
print(train_set.show(50))
print(val_set.show(50))
print(test_set.show(50))


tokenizer = Tokenizer(inputCol="Review", outputCol="words")
hashtf = HashingTF(numFeatures=2**16, inputCol="words", outputCol='tf')
idf = IDF(inputCol='tf', outputCol="features", minDocFreq=5)
label_stringIdx = StringIndexer(inputCol="Sentiment", outputCol="label")
pipeline = Pipeline(stages=[tokenizer, hashtf, idf, label_stringIdx])


pipelineFit = pipeline.fit(train_set)
train_df = pipelineFit.transform(train_set)
val_df = pipelineFit.transform(val_set)
print(train_df.show(5))

lr = LogisticRegression(maxIter=100)
lrModel = lr.fit(train_df)

predictions = lrModel.transform(val_df)
evaluator = BinaryClassificationEvaluator(rawPredictionCol="rawPrediction")
evaluator.evaluate(predictions)


accuracy = predictions.filter(predictions.label == predictions.prediction).count() / float(val_set.count())
print(accuracy)


tokenizer = Tokenizer(inputCol="Review", outputCol="words")
cv = CountVectorizer(vocabSize=2**16, inputCol="words", outputCol='cv')
idf = IDF(inputCol='cv', outputCol="features", minDocFreq=10)
label_stringIdx = StringIndexer(inputCol="Sentiment", outputCol="label")
lr = LogisticRegression(maxIter=100)
pipeline = Pipeline(stages=[tokenizer, cv, idf, label_stringIdx, lr])

pipelineFit = pipeline.fit(train_set)
predictions = pipelineFit.transform(val_set)
accuracy = predictions.filter(predictions.label == predictions.prediction).count() / float(val_set.count())
roc_auc = evaluator.evaluate(predictions)

print("Accuracy Score: {0:.4f}".format(accuracy))
print("ROC-AUC: {0:.4f}".format(roc_auc))
