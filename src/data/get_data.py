import src.db.db_utils as db
from src.data import process_df as pdf

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import operator

import time

from contextlib import closing
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


def get_local_dataset():
    return pd.read_csv('../../DataSet/Hotel_Reviews.csv')


def get_webscraped_data():
    positive_list, negative_list = [], []

    for i in range(2):
        page = requests.get('https://www.tripadvisor.com/Hotel_Review-g188590-d249326-Reviews-or' + str(i*5)
                            + '-Hotel_Arena-Amsterdam_North_Holland_Province.html#REVIEWS')
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            titles = soup.find_all('div', {'class': re.compile('hotels-review-list-parts-ReviewTitle__reviewTitle.+')})
            rating = soup.find_all('div', {'class': re.compile('hotels-review-list-parts-RatingLine__bubbles.+')})
            review = soup.find_all('q', {'class': re.compile('hotels-review-list-parts-ExpandableReview__reviewText.+')})
            for j in range(5):
                if (int(str(rating[j].span)[-11])) > 2:
                    positive_list.append({'Hotel_Name': 'Hotel Arena',
                                          'Positive_Review': str(review[j].span)[6:-7],
                                          'Reviewer_Score': str(rating[j].span)[-11]
                                          })
                else:
                    negative_list.append({'Hotel_Name': 'Hotel Arena',
                                          'Negative_Review': str(review[j].span)[6:-7],
                                          'Reviewer_Score': str(rating[j].span)[-11]
                                          })

    '''
    list_with_all_reviews = []
    with closing(Chrome(executable_path='C:/Users/quiri/Desktop/BDScientist-Engineer/Downloads/chromedriver.exe')) as driver:
        driver.get("https://uk.hotels.com/ho200999/hotel-arena-amsterdam-netherlands/?awc=8440_1571771494_f825cb913c5433a147a7d836133ba63a&locale=en_GB&pos=HCOM_UK&rffrid=aff.hcom.nl.011.000.324893.kwrd%3D8440_1571771494_f825cb913c5433a147a7d836133ba63a&wapb1=hotelcontentfeed")
        for i in range(1):
            button = driver.find_element_by_link_text("reviewTab=brand-reviews").click()
            time.sleep(5)
            # store it to string variable
            page_source = driver.page_source

            soup = BeautifulSoup(page_source, 'html.parser')
            reviews = soup.find_all('div', {'class': 'description'})
            scores = soup.find_all('div', {'class': 'rating-score'})

            print(reviews)
            for k in range(len(reviews)):
                if float(str(reviews[k].text)) > 5.5:
                    print(scores[k])
                    positive_list.append({'Hotel_Name': 'Via Amsterdam',
                                          'Positive_Review': reviews[k].text,
                                          'Reviewer_Score': scores[k].text})
                else:
                    negative_list.append({'Hotel_Name': 'Via Amsterdam',
                                          'Negative_Review': reviews[k].text,
                                          'Reviewer_Score': scores[k].text})
    '''
    return [negative_list, positive_list]


'''
    page = requests.get("https://www.hostelworld.com/hosteldetails.php/Via-Amsterdam/Amsterdam/280631#reviews")
    soup = BeautifulSoup(page.content, 'html.parser')
    reviews = soup.find_all('div', {'class': 'notes'})
    scores = soup.find_all('div', {'class': 'score'})
    for k in range(reviews):
        if scores[k] > 5.5:
            positive_list.append({'Hotel_Name': 'Via Amsterdam',
                                  'Positive_Review': reviews[k],
                                  'Reviewer_Score': scores[k]})
        else:
            negative_list.append({'Hotel_Name': 'Via Amsterdam',
                                  'Negative_Review': reviews[k],
                                  'Reviewer_Score': scores[k]})
'''


def get_own_reviews():
    positive_review = [
        'This hotel was great! I would recommend staying here',
        'Great hotel'
    ]

    negative_review = [
        'I dont like this hotel at all, Im not coming back',
        'Very bad service'
    ]

    return pd.DataFrame(np.column_stack([negative_review, positive_review]),
                        columns=['Negative_Review', 'Positive_Review'])


def upload_local():
    db.upload_to_db(pdf.process_df(get_local_dataset()), 'Kaggle')


def upload_web_scraped():
    reviews = get_webscraped_data()
    #df = pd.DataFrame(np.column_stack([reviews[0], reviews[1]]),
                      #columns=['Negative_Review', 'Positive_Review'])
    #db.upload_to_db(df, 'WebScraped')


def upload_written_reviews():
    db.upload_to_db(get_own_reviews(), 'Written')


def get_all_data():
    scraped = get_webscraped_data()
    negative_reviews = map(operator.itemgetter('Negative_Review'), scraped[0])
    positive_reviews = map(operator.itemgetter('Positive_Review'), scraped[1])

    df_written = pd.DataFrame(get_own_reviews())
    df_local = pd.DataFrame(get_local_dataset())
    df_scraped = pd.DataFrame(np.column_stack(['Hotel Arena', negative_reviews, positive_reviews]),
                              columns=['Hotel_Name', 'Negative_Review', 'Positive_Review'])
    df = df_local.append(df_scraped, ignore_index=True)
    df = df.append(df_written, ignore_index=True)
    pd.set_option('display.max_columns', None)
    df = pdf.process_df(df)


upload_web_scraped()