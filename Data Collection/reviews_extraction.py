import pandas as pd
import re
from google_play_scraper import Sort, reviews_all

all_ids = []
review_count = []
review_all = []
count = 0
review_list = []

def get_reviews(ids):
    for val in ids:
        # chanding the format of google playstore ids to the keywords for google play scraper

        url = val[1]
        function = val[18]
        try:
            match = re.search('id=(.*)', url)
        except Exception as inst:
            # print(inst)
            continue
        if match:
            id = match.group(1)
        else:
            print("No ID error")
            continue
        # print(id)
        reviews = reviews_all(
            id,
            sleep_milliseconds=0, # defaults to 0
            lang='en', # defaults to 'en'
            country='us', # defaults to 'us'
            sort=Sort.MOST_RELEVANT, # defaults to Sort.MOST_RELEVANT
            filter_score_with= None# defaults to None(means all score)
        )
        for review in reviews:
            review_dict = {
                "App ID": id,
                "Score": review["score"],
                "Review_text": review["content"],
                "Function": function
            }
            review_list.append(review_dict)
    review_count.append(len(reviews))
    review_all = review_all+reviews

    reviews_df = pd.DataFrame(review_list)

    return reviews_df

if __name__ == '__main__':

    
    input_file = 'app_details.csv' # load all the apps that we extracted from google playstore 

    df = pd.read_csv(input_file) 
    ids = df['app_id'] # for review extraction we are only using the app ids
    reviews_df = get_reviews(ids)
    reviews_df.to_csv('reviews.csv')

