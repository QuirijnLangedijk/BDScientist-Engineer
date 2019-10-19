import src.db.db_utils as db
from src.data import process_df as pdf
import pandas as pd
from bs4 import BeautifulSoup
import requests
import re


def get_local_dataset():
    return pd.read_csv('../../DataSet/Hotel_Reviews.csv')


def get_webscraped_data():
    data = []
    '''
    for i in range(200):
        page = requests.get('https://www.tripadvisor.com/Hotel_Review-g188590-d249326-Reviews-or' + str(i*5)
                            + '-Hotel_Arena-Amsterdam_North_Holland_Province.html#REVIEWS')
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            titles = soup.find_all('div', {'class': re.compile('hotels-review-list-parts-ReviewTitle__reviewTitle.+')})
            rating = soup.find_all('div', {'class': re.compile('hotels-review-list-parts-RatingLine__bubbles.+')})
            review = soup.find_all('q', {'class': re.compile('hotels-review-list-parts-ExpandableReview__reviewText.+')})
            for j in range(5):
                data.append(['Hotel Arena', str(rating[j].span)[-11], str(review[j].span)[6:-7]])
    '''

    for i in range(3):
        page = requests.get('https://www.alexander.co.il/hotel-alexander-reviews?reviews-page=' + str(i))

        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            reviews = soup.find_all('span', {'class': 'home-add-cont hidden'})
            short_reviews = soup.find_all('div', {'class': 'review-content'})
            ratings = soup.find_all('span', {'itemprop': 'ratingValue'})
            for i in range(len(reviews)):
                print(ratings[i].text.strip())
                data.append(['Hotel Alexander', ratings[i].text.strip(), reviews[i].text.strip()])
    df = pd.DataFrame(data, columns=['HotelName', 'Rating', 'Review'])
    pd.set_option('display.expand_frame_repr', False)
    print(df)
    return df


def get_own_reviews():
    print('s')


def upload_local():
    db.upload_to_db(pdf.process_df(get_local_dataset()), 'Kaggle')


def upload_web_scraped():
    db.upload_to_db(get_webscraped_data(), 'WebScraped')


def upload_written_reviews():
    db.upload_to_db(pdf.process_df(get_own_reviews()), 'Written')


# upload_local()
# upload_web_scraped()