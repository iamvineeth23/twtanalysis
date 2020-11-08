#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 18:25:21 2020

@author: vinnie
"""

import tweepy
from collections import defaultdict
import pandas as pd
import argparse
import os
from stats import tweet_analyzer

from keys import (
    api_key,
    api_secret_key,
    access_token,
    access_token_secret
)


auth = tweepy.OAuthHandler(api_key, api_secret_key)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)


class GetTweets:
    
    def __init__(self, api, userid, include_rts = False):
        self.userid = userid
        self.include_rts = include_rts
        
        print('Fetching tweets of: ', self.userid)
        
        self.tweets = api.user_timeline(screen_name = self.userid, count = 200, include_rts = self.include_rts, tweet_mode = 'extended')
        self.tweets_dict = defaultdict(list)
        self.acc_info = self.tweets[0].user
            
            
    def __check_if_retweet(self, obj):
    
        if hasattr(obj, 'retweeted_status'):
            return True
        
        return False


    def __get_hashtags(self, hashtags):
        
        tags_list = []
        
        for tags in hashtags:
            tags_list.append(tags['text'])
    
        return tags_list


    def __get_account_info(self):
        
        twt = self.acc_info
        
        print(f'\n \nName:\t {twt.name}')
        print(f'Description: {twt.description}' )
        print(f'Followers: {twt.followers_count}\t Follwing: {twt.friends_count}' )
        print(f'Account created on: {twt.created_at}\t Location: {twt.location}\n')
        
        with open("data/info" + self.userid, "w") as text_file:
            text_file.write(f'Name: {twt.name}\n Description: {twt.description}\n \
                            Followers: {twt.followers_count}\t Follwing: {twt.friends_count}\n \
                            Account created on: {twt.created_at}\t Location: {twt.location}')
    
        
    def __build_dictionary(self):
        
        for status in self.tweets:

            self.tweets_dict['id'].append(status.id_str)
            self.tweets_dict['favourite_count'].append(status.favorite_count)
            self.tweets_dict['created_at'].append(status.created_at)
            self.tweets_dict['retweet_count'].append(status.retweet_count)
            self.tweets_dict['tweet'].append(status.full_text)
            self.tweets_dict['tags'].append(self.__get_hashtags(status.entities.get('hashtags')))
            
            tweet_url = 'https://twitter.com/twitter/status/' + status.id_str
            self.tweets_dict['tweet_url'].append(tweet_url)
            
            if not self.include_rts:
                self.tweets_dict['is_retweet'].append(self.__check_if_retweet(status))

    def fetch_tweets(self):

        oldest_id = self.tweets[-1].id

        self.__build_dictionary()
        
        n_tweets = len(self.tweets)

        while True:
            
            print('Tweets fetched till now {}'.format(n_tweets))
            
            
            self.tweets = api.user_timeline(screen_name = self.userid,
                                            count = 200, include_rts = False,
                                            max_id = oldest_id - 1,
                                            tweet_mode = 'extended')
            n_tweets += len(self.tweets)
            
            if len(self.tweets)  == 0:
                break
            
            oldest_id = self.tweets[-1].id
            self.__build_dictionary()
        
        self.__get_account_info()
        return pd.DataFrame.from_dict(self.tweets_dict) 


    def save_obj(self, df, name):
        
        df.to_csv('data/'+ name + '.csv', index=False)
                
        
        
def main(USERID):
    

    t1 = GetTweets(api, USERID)
    tweets_df = t1.fetch_tweets()
    t1.save_obj(tweets_df, USERID)
    
    analyzer = tweet_analyzer(tweets_df, plot=True)
    analyzer.get_stats()


if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Get statistical analysis on tweeter users')
    
    parser.add_argument("-u", "--user", required=False, dest="user",
                        help="u/user_name to fetch the tweets", metavar="TWT_USER")
    
    args = parser.parse_args()
    user = args.user
    
    if not (os.path.isdir('data')):
        os.mkdir('data') 
        
        
    main(user)
