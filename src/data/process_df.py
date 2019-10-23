import pandas as pd


def process_df(df):
    df.drop(['Additional_Number_of_Scoring', 'Review_Date', 'Reviewer_Nationality', 'Total_Number_of_Reviews', 'Total_Number_of_Reviews_Reviewer_Has_Given', 'days_since_review', 'Tags', 'lat', 'lng'], inplace=True, axis=1)
    df = df.drop(df[(df['Negative_Review'].str.contains("(?i)no negative|nothing|none")) |
                    (df['Positive_Review'].str.contains("(?i)no positive|nothing|none"))
                    ].index)
    df.reset_index(drop=True, inplace=True)
    pd.set_option('display.max_columns', None)
    return df
