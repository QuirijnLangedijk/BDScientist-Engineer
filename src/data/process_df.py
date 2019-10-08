import pandas as pd


def process_df(df):
    df.drop(['Additional_Number_of_Scoring', 'Review_Date', 'Reviewer_Nationality', 'Total_Number_of_Reviews', 'Total_Number_of_Reviews_Reviewer_Has_Given', 'days_since_review', 'lat', 'lng'], inplace=True, axis=1)
    df.replace('No Negative', '')
    df.replace('No Positive', '')
    # df = df.drop(df[(df['Negative_Review'] == 'No Negative') | (df['Positive_Review'] == 'No Positive')].index)
    return df
