import tweepy
import credentials #file with consumer_key, consumer_secret, access_token and access_token_secret
import pandas as pd
import os

auth = tweepy.OAuthHandler(credentials.consumer_key, credentials.consumer_secret)
auth.set_access_token(credentials.access_token, credentials.access_token_secret)

#initialize Tweepy API
api = tweepy.API(auth, wait_on_rate_limit=True)

def search_for_hashtags(hashtag_phrase, name_data, columns=list()):
    
    tweets_data = []
    for tweet in tweepy.Cursor(api.search, q=hashtag_phrase+' -filter:retweets',lang="en").items(1000):
        tweet_dict = dict(vars(tweet))
        keys = tweet_dict.keys()
        single_tweet_data = {'user': tweet.user.screen_name, 'author': tweet.author.screen_name}
        for key in keys:
            if key in columns:
                single_tweet_data[key] = tweet_dict[key]
        tweets_data.append(single_tweet_data)

    columns.append('user')
    columns.append('author')
    if not os.path.exists('./Data/'):
        os.makedirs('./Data/')
    df = pd.DataFrame(tweets_data, columns=columns)
    df.to_csv(f'./Data/{name_data}.csv', sep=';')
    
    
if __name__ == '__main__':
    
    hashtag_phrase = input('Hashtag Phrase ')
    columns = input('Which columns do you want ? ')
    name_data = input('Data name ')
    search_for_hashtags(hashtag_phrase, name_data, columns)