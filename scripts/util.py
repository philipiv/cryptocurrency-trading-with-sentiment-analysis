import json

import pandas as pd
import numpy as np


def get_config(config_file):

    """
    This function loads configuration file with all necessary api keys into memory.

    input:
        - config_file: configuration file path

    output:
        - config: dictionary containing configuration file
    """

    with open(config_file) as json_file:
        config = json.load(json_file)

    return config


def get_signal_norm_dates(signal_, index):
    """
    This function takes a time series and an index and creates a new time series
    with the former information into the given index.
    As new index may contain more dates, interpolation may be needed.

    input:
        - signal_: time series
        - index: array of dates

    output:
        - signal: time series from input expressed into new index
    """

    signal = pd.Series(index=index)

    signal[signal_.index] = signal_
    signal = signal.interpolate()

    return signal


def get_sentiment(index, query, tweepy_keys):

    """
    This function computes the sentiment analysis for the given date range.

    input:
        - index: range of dates to search
        - query: word or sentence to search in tweeter api

    output:
        - sentiment: pandas Series with sentiment analysis
    """

    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    import tweepy

    auth = tweepy.OAuthHandler(tweepy_keys['consumer-token'], tweepy_keys['consumer-secret'])
    auth.set_access_token(tweepy_keys['access-token'], tweepy_keys['access-secret'])

    api = tweepy.API(auth)

    sentiment = pd.Series(index=index)

    for date in index:

        date_plus_one = date + pd.Timedelta(days=1)

        searchtweets = api.search(q=query, count=100,
                                  lang="en",
                                  since=date,
                                  until=date_plus_one,
                                  tweet_mode='extended')

        sentences=[]
        for result in searchtweets:

            sentences.append(result.full_text)
        
        vs = 0
        analyzer = SentimentIntensityAnalyzer()
        for sentence in sentences:
            vs = vs + analyzer.polarity_scores(sentence)['compound']

        if np.shape(sentences)[0] != 0: vs = vs / np.shape(sentences)[0]

        sentiment[date] = vs

    return sentiment
