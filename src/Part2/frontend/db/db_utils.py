import pymongo
import pandas as pd

CONNECTION_STRING = "mongodb+srv://admin:admin@cluster0-n8kmr.gcp.mongodb.net/test?retryWrites=true&w=majority"


def clean(df):
    df = df.drop(df[(df['Negative_Review'].str.contains("(?i)no negative|nothing|none|n a|na|all positive|all good|everything")) |
                    (df['Positive_Review'].str.contains("(?i)no positive|nothing|none|n a|na|all negative|everything"))
                    ].index)

    df = df[df.Negative_Review.str.strip() != '']
    df = df[df.Positive_Review.str.strip() != '']

    df.reset_index(drop=True, inplace=True)
    return df


def upload_all_data():
    df = pd.read_csv('../../../DataSet/Hotel_Reviews.csv')
    column_names = ['Hotel_Address', 'Hotel_Name', 'Lat', 'Lng', 'Average_Score', 'Total_Number_of_Reviews',
                    'Additional_Number_of_Scoring', 'Reviewer_Nationality', 'Review_Date', 'Review', 'Review_Word_Counts',
                    'Total_Number_of_Reviews_Reviewer_Has_Given', 'Reviewer_Score', 'Tags', 'Sentiment']

    df = clean(df)
    client = pymongo.MongoClient('localhost', 27017)
    db = client.PO2.all_data

    for index, row in df.iloc[3000:].iterrows():

        positive_data = [row['Hotel_Address'], row['Hotel_Name'], row['lat'], row['lng'], row['Average_Score'],
                         row['Total_Number_of_Reviews'], row['Additional_Number_of_Scoring'], row['Reviewer_Nationality'],
                         row['Review_Date'], row['Positive_Review'], row['Review_Total_Positive_Word_Counts'], row['Total_Number_of_Reviews_Reviewer_Has_Given'],
                         row['Reviewer_Score'], row['Tags'], '1']

        negative_data = [row['Hotel_Address'], row['Hotel_Name'], row['lat'], row['lng'], row['Average_Score'],
                         row['Total_Number_of_Reviews'], row['Additional_Number_of_Scoring'], row['Reviewer_Nationality'],
                         row['Review_Date'], row['Negative_Review'], row['Review_Total_Negative_Word_Counts'], row['Total_Number_of_Reviews_Reviewer_Has_Given'],
                         row['Reviewer_Score'], row['Tags'], '0']

        review = pd.DataFrame([positive_data, negative_data], columns=column_names)
        db.insert_many(review.to_dict(orient='records'))


def upload_balanced_data():
    df = pd.read_csv('../../../DataSet/Hotel_Reviews.csv')
    df = clean(df)
    client = pymongo.MongoClient('localhost', 27017)
    db = client.PO2.balanced_data3

    for i in range(10000):
        if len(df.iloc[i].Positive_Review) > 0 and len(df.iloc[i].Negative_Review) > 0:
            positive_data = [df.iloc[i].Positive_Review, 1]
            negative_data = [df.iloc[i].Negative_Review, 0]
            review = pd.DataFrame([positive_data, negative_data], columns=['text', 'label'])
            db.insert_many(review.to_dict(orient='records'))


def get_balanced_data():
    client = pymongo.MongoClient('localhost', 27017)
    col = client.PO2.balanced_data
    cursor = col.find()
    df = pd.DataFrame(list(cursor))

    del df['_id']
    return df


def get_all_data():
    return execute_query('all_data')


def execute_query(collection, query=''):
    client = pymongo.MongoClient('localhost', 27017)
    col = client.PO2[collection]
    print(col)
    print(query)
    cursor = col.aggregate(query, allowDiskUse=True)

    df = pd.DataFrame(list(cursor))

    return df
