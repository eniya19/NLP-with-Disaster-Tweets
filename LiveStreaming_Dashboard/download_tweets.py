import tweepy
import pandas as pd
import datetime




def get_download_tweets(api, search_keyword, number_of_tweets = 10):
    """
    This Function will download tweets from twitter
    Input:
        a) api(object): Twitter api object
        b) search_keyword(str): The keyword which is needed to be searched

    Output:
        a) tweet_date_dict(dict): Dictonary consisting of tweet date and tweets
    """

    date = datetime.date.today() - datetime.timedelta(1)

    since_date = date
    end_date = date
    search_api = tweepy.Cursor(api.search, q=[search_keyword], lang="en", since=since_date).items(number_of_tweets)
    searched_tweets_result  = [status._json for status in search_api]
    tweet_text_list = []
    tweet_date_list = []
    tweet_date_dict = {}
    for tweet in searched_tweets_result:
        date = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y').strftime('%Y-%m-%d %H:%M:%S')
        str_tweet = tweet['text']
        tweet_text_list.append(str_tweet)
        tweet_date_list.append(date)
    tweet_date_dict = dict(zip(tweet_date_list, tweet_text_list))
    return tweet_date_dict
