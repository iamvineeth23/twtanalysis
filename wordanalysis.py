#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 19:45:37 2020

@author: vinnie
"""

from ast import literal_eval
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re


class WordsAnalysis:
    
    
    def __init__(self, df):
        
        self.df = df        
        

    def __count_tags(self):
        
        all_tags = []
        for a in self.df['tags']:
    
            all_tags.extend(literal_eval(a))
        
        
        self.tag_count = Counter(all_tags)
        cnts_per = [(i, self.tag_count[i] / len(all_tags) * 100.0) for i, count in self.tag_count.most_common()]

        self.top_tags_per = [cnts_per[i][1] for i in range(5)]
        self.tag_labels = [cnts_per[i][0] for i in range(5)]
        
        self.top_tags_per.append(100-sum(self.top_tags_per))
        self.tag_labels.append("others")


    
    def __process_tweets(self, tweets):
        
        ps = PorterStemmer()

        corpus = []
        
        for t in tweets:
            
            review = re.sub(r'http\S+', '', t)
        
            review = re.sub('[^a-zA-Z]', ' ', review)
            review = review.lower()
            review = review.split()
            review = [ps.stem(word) for word in review if not word in set(stopwords.words('english'))]
            review = ' '.join(review)
            corpus.append(review)
    
        big_words_list = []
        for word in corpus:
            
            big_words_list.extend(word.split())

        return big_words_list
    

    def __count_words(self):


        tweets = self.df['tweet']
        big_words_list = self.__process_tweets(tweets)
        
        self.words_count = Counter(big_words_list)
        cnts_per = [(i, self.words_count[i] / len(big_words_list) * 100.0) for i, count in self.words_count.most_common()]
        
        self.top_words_per = [cnts_per[i][1] for i in range(5)]
        self.word_labels = [cnts_per[i][0] for i in range(5)]
        
        self.top_words_per.append(100-sum(self.top_words_per))
        self.word_labels.append("others")
        
        
    def __create_wordcloud(self, count, name):
        
        
        wordcloud = WordCloud(max_font_size=250,collocations=False, background_color="white", width=1600, height=800).generate(" ".join([(k + ' ') * v for k,v in count.items()]))
        plt.figure(figsize=(10,5))
        plt.tight_layout(pad=0)
        plt.imshow(wordcloud, interpolation="bilinear")
        plt.axis("off")
        plt.savefig('data/' + name + '.png', dpi=300)
        plt.show()
        
    
    def analyse(self):
        
        self.__count_tags()
        self.__count_words()
        
        self.__create_wordcloud(self.tag_count, 'tags_cloud')
        self.__create_wordcloud(self.words_count, 'words_cloud')
        
  
        
if __name__ == "__main__":
    pass

        
# import pandas as pd

# df = pd.read_csv('data/isro.csv')

# wa = WordsAnalysis(df)
# wa.analyse()

