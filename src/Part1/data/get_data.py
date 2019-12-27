import src.Part1.db.db_utils as db
from src.Part1.data import process_df as pdf

import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests
import re
import time
from contextlib import closing
from selenium.webdriver import Chrome


def get_local_dataset():
    return pd.read_csv('../../../DataSet/Hotel_Reviews.csv')


def get_webscraped_data():
    positive_list, negative_list = [], []

    for i in range(2):
        if i % 10 == 0:
            print(i)
        page = requests.get('https://www.tripadvisor.com/Hotel_Review-g188590-d249326-Reviews-or' + str(i * 5)
                            + '-Hotel_Arena-Amsterdam_North_Holland_Province.html#REVIEWS')
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            rating = soup.find_all('div', {'class': re.compile('hotels-review-list-parts-RatingLine__bubbles.+')})
            review = soup.find_all('q',
                                   {'class': re.compile('hotels-review-list-parts-ExpandableReview__reviewText.+')})
            for j in range(5):
                if (int(str(rating[j].span)[-11])) > 2:
                    positive_list.append(str(review[j].span)[6:-7])
                else:
                    negative_list.append(str(review[j].span)[6:-7])

    with closing(
            Chrome(executable_path='../../../Downloads/chromedriver.exe')) as driver:
        driver.get("https://www.trivago.co.uk/?cpt2=47362%2F100&sharedcid=47362&tab=rating")

        # Sleep to load pages.
        time.sleep(3)
        button = driver.find_elements_by_class_name("tabs__label")
        time.sleep(1)
        button[3].click()
        time.sleep(1)
        see_more = driver.find_elements_by_class_name("td-underline--hover")[1].click()
        time.sleep(2)
        page_source = driver.page_source

        soup = BeautifulSoup(page_source, 'html.parser')
        # Find all scores and reviews.
        reviews = soup.find_all('p', {'class': 'sl-review__summary'})
        scores = soup.find_all('span', {'class': 'item-components__pillValue--4748f item-components__value-med--a26b7 item-components__pillValue--4748f'})
        clean_reviews = [x for x in reviews if x.text[len(x.text)-4:len(x.text)] == "...." or not x.text[len(x.text)-3:len(x.text)] == '...']

        # Loop over reviews, discard reviews with no score (/).
        for k in range(len(clean_reviews)):
            if scores[k].text != "/":
                if float(scores[k].text) > 5.5:
                    positive_list.append(str(reviews[k].text))
                elif float(scores[k].text) < 5.5:
                    negative_list.append(str(reviews[k].text))

    return [negative_list, positive_list]


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
    print(pdf.process_df(get_local_dataset()), 'Kaggle')
    #db.upload_to_db(pdf.process_df(get_local_dataset()), 'Kaggle')


def upload_web_scraped():
    reviews = get_webscraped_data()
    negative = reviews[0]
    positive = reviews[1]
    dict_1 = {
        'Negative_Review': negative,
        'Positive_Review': positive
    }
    df = pd.DataFrame.from_dict(dict_1, orient='index')
    df = df.transpose()
    db.upload_to_db(df, 'WebScraped')


def upload_written_reviews():
    db.upload_to_db(get_own_reviews(), 'Written')


def upload_all_data():
    upload_local()
    upload_web_scraped()
    upload_written_reviews()


def get_all_kaggle():
    return db.get_from_db(f'CALL GetKaggleSet()')


def get_all_scraped():
    return db.get_from_db(f'CALL GetWebScrapedSet()')


def get_all_written():
    return db.get_from_db(f'CALL GetWrittenSet()')


def get_all_data():
    dataset = get_all_kaggle()
    scraped = get_all_scraped()
    written = get_all_written()
    dataset = dataset.append(scraped)
    dataset = dataset.append(written)
    dataset.reset_index(drop=True, inplace=True)
    return dataset

upload_local()