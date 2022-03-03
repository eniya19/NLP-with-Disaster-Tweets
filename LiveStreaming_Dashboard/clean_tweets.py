import re
import nltk
import nltk.sentiment
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
from collections import Counter



def get_clean_tweets(raw_tweet):
    clean_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", raw_tweet).split())

    clean_tweet = re.sub(r"http\S+", "", clean_tweet)

    return clean_tweet

def get_word_tokenize_list(asset_data_list, stopwords_list):

    final_asset_word_tokenize_list = []

    for article in asset_data_list[:]:
        # Cleaning the article
        clean_article = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w+:\/\/\S+)", " ", article).split())
        clean_article = re.sub('\W+',' ', clean_article)

        # Tokenizing the article
        current_word_tokenize_list = word_tokenize(clean_article)

        # Removing Stopwords
        current_word_tokenize_list = [x for x in current_word_tokenize_list if x not in stopwords_list]

        final_asset_word_tokenize_list.extend(current_word_tokenize_list)

    return final_asset_word_tokenize_list

def get_top_trending_words(asset_data_list, stopwords_list):

    # Getting word tokenize list
    final_asset_word_tokenize_list = get_word_tokenize_list(asset_data_list, stopwords_list)

    # Word Frequency Distribution
    word_frequency_dict = dict(Counter(final_asset_word_tokenize_list))

    # Sorting Frequency Distribution in a reverse Order.

    top_trending_words_list = sorted(word_frequency_dict.items(), key=lambda x: x[1], reverse=True)
    top_trending_words_dict = dict(top_trending_words_list)

    return top_trending_words_dict
