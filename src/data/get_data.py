from src.db import db_utils as db
from src.data import process_df as pdf
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


def get_local_dataset():
    return pd.read_csv('../../DataSet/Hotel_Reviews.csv')


def get_webscraped_data():
    data = []
    for i in range(200):
        page = requests.get('https://www.tripadvisor.com/Hotel_Review-g188590-d249326-Reviews-or' + str(i*5) + '-Hotel_Arena-Amsterdam_North_Holland_Province.html#REVIEWS')
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            titles = soup.find_all('div', {'class': re.compile('hotels-review-list-parts-ReviewTitle__reviewTitle.+')})
            rating = soup.find_all('div', {'class': re.compile('hotels-review-list-parts-RatingLine__bubbles.+')})
            review = soup.find_all('q', {'class': re.compile('hotels-review-list-parts-ExpandableReview__reviewText.+')})
            for j in range(5):
                data.append([str(titles[j].span)[12:-14], str(rating[j].span)[-11], str(review[j].span)[6:-7]])
    return pd.DataFrame(data, columns=['Title', 'Rating', 'Review'])


def get_own_reviews():
    print('s')


def get_all_data():
    local = get_local_dataset()
    # scraped = get_webscraped_data()
    # own = get_own_reviews()
    return local


def upload_data_to_db():
    db.upload_to_db(pdf.process_df(get_all_data()))

# upload_data_to_db()