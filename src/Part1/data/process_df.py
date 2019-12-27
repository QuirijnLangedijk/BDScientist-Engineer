import pandas as pd

REGEX = "^(((\d|\w)*?\s?nothing\s?(\d|\w)*\s?)|none|null|((\d|\w)+\s?(negative|positive)))$"


def process_df(df):
    #df.drop(['Additional_Number_of_Scoring', 'Review_Date', 'Reviewer_Nationality', 'Total_Number_of_Reviews', 'Total_Number_of_Reviews_Reviewer_Has_Given', 'days_since_review', 'Tags', 'lat', 'lng'], inplace=True, axis=1)
    col_list = ['Negative_Review', 'Positive_Review']
    df = df[col_list]
    df = df.drop(df[(df['Negative_Review'].str.contains(REGEX)) |
                    (df['Positive_Review'].str.contains(REGEX))
                    ].index)
    df.reset_index(drop=True, inplace=True)
    df.dropna(inplace=True)
    # pd.set_option('display.max_columns', None)
    return df
