import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from io import BytesIO
import numpy as np
import pandas as pd
from wordcloud import WordCloud
import base64
import re
from nltk.corpus import stopwords
from dash.dependencies import Input, Output
import chart_studio as py
import plotly.graph_objs as go
import tweepy
import csv
import pandas as pd
import datetime
import re
import nltk
import textblob
import nltk.sentiment
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import dash_table
import download_tweets
import clean_tweets
import plotly.express as px
import random

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport",
    "content": 'width=device-width, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0,'
}]
)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = app.server

consumer_key = '4nEKcrfvVoP2bSzbLwmaKS6ls'
consumer_secret = 'rsU38b4pzi0PxTYBHoHrdr9LqdddtCtLgjkeTuwTxZvMW9ixpj'


auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth,wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


def get_target_predicted():
    with open('disaster_prediction', 'rb') as f:
    x = pickle.load(f)
    return random.randint(0,1)

def update_tweet_data(search_value, number_of_tweets=10):
    tweet_date_dict = download_tweets.get_download_tweets(api, search_value, number_of_tweets)
    final_df = pd.DataFrame()
    for date,tweet in tweet_date_dict.items():
        date = date
        raw_tweet = tweet
        clean_tweet_text = clean_tweets.get_clean_tweets(raw_tweet)
        target = get_target_predicted()
        print(date, clean_tweet_text)
        tweets_df = pd.DataFrame({'date':date, 'tweet':raw_tweet, 'target':target},
        index=[0], columns=['date', 'tweet', 'target'])
        final_df = final_df.append(tweets_df)

    final_df.sort_values(['date'], ascending=True, inplace=True)
    final_df.to_csv('tweets.csv')


def get_top_trending_graph(tweets_df):
    tweets_data_list = tweets_df["tweet"].to_list()
    stopwords_list = set(stopwords.words('english'))
    top_trending_words_dict = clean_tweets.get_top_trending_words(tweets_data_list, stopwords_list)
    trending_df = pd.DataFrame({"words":list(top_trending_words_dict.keys()), "frequency":list(top_trending_words_dict.values())})[:10]

    trending_df["percentage"] = round(trending_df["frequency"] /trending_df["frequency"].sum(), 2) * 100
    trending_df = trending_df.sort_values("percentage", ascending=True)
    trending_df["words"] = trending_df["words"].apply(lambda x:x.capitalize())
    fig = go.Figure()

    fig =  fig.add_trace(
            go.Bar(
                x=trending_df["percentage"],
                y=trending_df["words"],
                orientation='h',
            ))

    layout ={
            'xaxis': {'range': [0, 100], 'title': 'Percentage', 'showgrid':True, 'gridcolor':'#3E3F40', 'gridwidth':1},
            'title': 'Top Trending Words',
            'yaxis': {'autorange': True, 'title': 'Top Trending Word'},
            'margin':{"r":25,"t":25,"l":25,"b":25},
            'paper_bgcolor':"white",
            'plot_bgcolor':"white",
            'font': {"color": "black"},

            }
    fig.update_layout(layout)

    return fig

def plot_wordcloud(tweets_df):
    tweets_data_list = tweets_df["tweet"].to_list()
    stopwords_list = set(stopwords.words('english'))
    top_trending_words_dict = clean_tweets.get_top_trending_words(tweets_data_list, stopwords_list)
    trending_df = pd.DataFrame({"words":list(top_trending_words_dict.keys()), "freq":list(top_trending_words_dict.values())})

    d = {x:a for a, x in trending_df.values}

    wc = WordCloud(background_color='white', width=880, height=360)
    wc.fit_words(d)
    return wc.to_image()


tweets_graph_layout = html.Div(children=[
    html.Div(children=[
        html.Div(id='tweets_pie_pos_chart_graph'),
    ],className='box card five columns'),
    html.Div(children=[
        dcc.Graph(id='output_twitter_top_treding_graph',config={'displayModeBar': False}),
    ],className='box card five columns'),
],className='container twelve columns')



word_twitter_count_graph = html.Div(children=[
    html.Div(children=[
        html.Img(id='image_wc_twitter', style={'height':'98%', 'width':'98%'}),
    ],className='box card eleven columns'),
],className='container twelve columns')



app.layout = html.Div(
    children = [
        html.Div(
            id="banner",
            className="twelve columns",
            children=[
             dcc.Tabs([
                 dcc.Tab(children=[

                    html.H1('Tweets Sentiment Analysis', style={"font-family": "Sans-serif", "text-align": "center",'fontSize': 30, 'color': "white", "padding":"20px",
                     "backgroundColor":"blue", "box-shadow": "0 8px 16px 0 rgba(0,0,0,1)", "border-radius": "10px"}),
                    html.Div([
                        html.Div([
                            dcc.Input(id='tweets_input_search', type='text', placeholder='Enter a text to Search', style={'width': '80%', 'height': 100})
                            ]),
                        html.Button('Submit', id='tweets_button')

                        ], style={"font-family": "Sans-serif", "text-align": "center",'fontSize': 30, 'color': "white", #"padding":"20px",
                        "width":"100%", 'display': 'inline-block'}
                        ),
                     tweets_graph_layout,
                     word_twitter_count_graph,
                     html.Div(id='tweets_table',className='sentiment_container')
                 ]),
             ])

        ]),
    ])



# Twitter Sentiment Graph
@app.callback(
    [dash.dependencies.Output('tweets_pie_pos_chart_graph', 'children'),
    dash.dependencies.Output('image_wc_twitter', 'src'),
    dash.dependencies.Output('output_twitter_top_treding_graph', 'figure')],
    [dash.dependencies.Input('tweets_button', 'n_clicks'),
    dash.dependencies.Input('image_wc_twitter', 'id')],
    [dash.dependencies.State('tweets_input_search', 'value')])
def update_output(n_clicks, b,value):
    if value == None:
        value = '#Flood'
    print(value)
    update_tweet_data(value)
    tweets_df = pd.read_csv('tweets.csv')
    tweets_df = tweets_df[['date', 'tweet', 'target']]
    target_list = tweets_df['target'].to_list()

    disaster_count = target_list.count(1)
    non_disaster_count = target_list.count(0)
    print(disaster_count, non_disaster_count)



    """ Pie Disaster , Non Disaster Chart """
    pie_data =  dcc.Graph(id='pie-live-chart',
                    figure= {
                    'data' : [go.Pie(values=[disaster_count, non_disaster_count], labels=['Disaster', 'Non Disaster'],
                    marker = {'colors': ['#22f20d', '#e33d1a'], 'line':dict(color='#000000', width=2)})]

                    })


    """ Word Cloud """
    img = BytesIO()
    plot_wordcloud(tweets_df).save(img, format='PNG')
    word_cloud_image ='data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())

    """ Top Trending Graph """
    top_trending_graph = get_top_trending_graph(tweets_df)

    return pie_data,word_cloud_image, top_trending_graph

if __name__ == "__main__":
    app.run_server(debug=True)
