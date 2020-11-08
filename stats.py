#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 10:37:53 2020

@author: vinnie
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pickle 
import pandas as pd
import calendar
import locale
import seaborn as sns

locale.setlocale(locale.LC_ALL, 'en_US.utf8')


class tweet_analyzer:
    
    def __init__(self, df, plot=True):
        
        self.plot   = plot         
        self.df     = df.sort_values(by=['created_at'])
              
    def __printer_help(self, var, title):
        
        print(f'\n------------------------{title}----------------------------')
    
        for index, row in var.iterrows():
            
            print("\nTweeted at: ", row['created_at'] )
            print("Favourites: {} \t Retweets: {}" .format(row['favourite_count'], row['retweet_count']))
            print(row['tweet'])
            print("Link: ", row['tweet_url'])
            
        print(f'-------------------------------------------------------------')
            
        
    def __calculate_averages(self):

        self.index = self.df['created_at']
        self.index = [pd.to_datetime(date, format='%Y-%m-%d').date() for date in self.index]

        self.df['created_at'] = pd.DataFrame(self.index, columns=['date'])
        self.df['created_at'] = pd.to_datetime(self.df['created_at'])
        self.df['days'] = self.df['created_at'].dt.day_name()
        
        bins = self.df[['days', 'created_at', 'favourite_count', 'retweet_count']].reset_index()
        bins['freq'] = bins.groupby('created_at')['created_at'].transform('count')
        
        temp = bins[['days', 'created_at', 'freq']]
        temp = temp.drop_duplicates()
        avg_day = temp.groupby(['days']).mean().reset_index()
        
        cats = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday' ] 
        
        self.averages = bins.groupby(['days']).mean().reset_index()
        self.averages['freq'] = avg_day['freq']
        
        self.averages['days'] = pd.Categorical(self.averages['days'], categories=cats, ordered=True)
        self.averages = self.averages.sort_values('days')
        self.averages = self.averages.drop(columns=['index'])
        
        cats = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ]
        self.averages['days'] = cats


    def __plot_stats(self):

        fig1 = plt.figure(figsize=(13,10), constrained_layout=True)

        gs = fig1.add_gridspec(3, 3)
        
        f1_ax1 = fig1.add_subplot(gs[0, :])
        plt.plot(self.index, self.df['favourite_count'], linewidth=1.5)
        y_mean = [np.mean(self.df['favourite_count'])]*len(self.index)
        plt.plot(self.index, y_mean, 'g--', label='average', linewidth=1.5)
        f1_ax1.grid(axis='y')    
        f1_ax1.set_title('Favourite over time',  fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        
        f1_ax2 = fig1.add_subplot(gs[1, :])
        plt.plot(self.index, self.df['retweet_count'], linewidth=1.5)
        y_mean = [np.mean(self.df['retweet_count'])]*len(self.index)
        plt.plot(self.index, y_mean, 'g--', label='average', linewidth=1.5)
        f1_ax2.grid(axis='y')    
        f1_ax2.set_title('Retweet over time',  fontsize=12)
        plt.xticks(fontsize=12)
        plt.yticks(fontsize=10)
        
        f1_ax3 = fig1.add_subplot(gs[-1:, -1])
        sns.barplot(x=self.averages['days'], y=self.averages['retweet_count'], palette="rocket")
        f1_ax3.grid(axis='y')
        f1_ax3.set_title('Avg. retweets per day')
        f1_ax3.set_ylabel('')
        f1_ax3.set_xlabel('')
        
        f1_ax4 = fig1.add_subplot(gs[-1, 0])
        sns.barplot(x=self.averages['days'], y=self.averages['freq'], palette="rocket")
        f1_ax4.grid(axis='y')
        f1_ax4.set_title('Avg. tweets per day')
        f1_ax4.set_ylabel('')
        f1_ax4.set_xlabel('')
        
        f1_ax5 = fig1.add_subplot(gs[-1, -2])
        sns.barplot(x=self.averages['days'], y=self.averages['favourite_count'], palette="rocket")
        f1_ax5.grid(axis='y')
        f1_ax5.set_title('Avg. favourites per day')
        f1_ax5.set_ylabel('')
        f1_ax5.set_xlabel('')
        
        fig1.savefig('data/stats.png', dpi=300)
        plt.show(block=True)

    def get_stats(self):
        
        most_liked  = self.df.sort_values(by=['favourite_count'], ascending=False)[:3]
        most_rtwt   = self.df.sort_values(by=['retweet_count'], ascending=False)[:3]
        
        # print stats 
        self.__printer_help(most_liked, "most favourited")
        self.__printer_help(most_rtwt, "most retweeted")
        self.__printer_help(self.df[:3], "most recent")

        self.__calculate_averages()
        print(self.averages.head())
        
        if self.plot:
            self.__plot_stats()
        
        
if __name__ == "__main__":
    pass
