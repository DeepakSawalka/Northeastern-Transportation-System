#!/usr/bin/env python
# coding: utf-8

# In[1]:


import tweepy #Library required for Twitter API
import csv, re
import pandas as pd
import os
import wget
import logging


# In[2]:


consumer_key = "fSK4WVeFeeTsJ1jQsdiVojC55"
consumer_secret = "e4LsMhBfKaUVclyV0T8tWlxR3xNMbusx6uEkzuI7QPLETmvS0e"
access_key = "1588319442013868032-WTXs6TTdoEXaoAD8yiy6iez7QmX85J"
access_secret="2UdaZ8XbkUkdm8jfTuK7qXQ2fjJx4pzspfCRzJducA0yE"


# In[194]:


#Creating an empty dataframe to store the information
tweets =pd.DataFrame(columns=["id","created_at","Text","Location","UserName","UserScreenname","Userfollwerscount","Userfavouritescount","User_Description","Retweet_Count","Source","Verified_Account",
                              "User_Account_Created","Status_Count","listed_counted"])


# In[195]:


tweets.columns


# In[196]:


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

try:
    api.verify_credentials()
    print("Authentication OK")
except:
    print("Error during authentication")


# In[197]:


get_ipython().system(' pip install pip')

import pip
package ='tweepy' #Just replace the package name with any package to install it.
pip.main(['install',package])


# In[213]:


import datetime, time
now = datetime.date.today()
date_since = datetime.datetime.strptime(time.strftime("%Y-%m-%d"), "%Y-%m-%d")
print (date_since)
keywords=['MBTA']
print (' '.join(keywords))
num_tweets=150
print ("num_tweets ", num_tweets)


# In[214]:


new_search = "MBTA -filter:retweets"


# In[215]:


# https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
# https://docs.tweepy.org/en/stable/api.html#search-tweets
tweets = tweepy.Cursor(api.search_tweets,
              q=new_search,
              lang="en",
              until=date_since).items(num_tweets)


# In[216]:


cnt=0
tweets_data = [] #initialize master list to hold our ready tweets
for tweet in tweets:
    print(cnt)    
    print(tweet)
    cnt=cnt+1


# In[217]:


# https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
# https://docs.tweepy.org/en/stable/api.html#search-tweets
tweets = tweepy.Cursor(api.search_tweets,
              q=new_search,
              lang="en",
              until=date_since).items(num_tweets)


# In[218]:


tweets


# In[219]:


cnt=0
tweets_data = [] #initialize master list to hold our ready tweets
for tweet in tweets:
    print(cnt)    
    tweets_data.append([tweet.id_str,tweet.created_at,tweet.text.encode("utf-8"),tweet.user.location,tweet.user.name,tweet.user.screen_name,tweet.user.followers_count,tweet.user.favourites_count,tweet.user.description,tweet.retweet_count,tweet.source,tweet.user.verified,tweet.user.created_at,tweet.user.statuses_count,tweet.user.listed_count])    
    cnt=cnt+1


# In[221]:


tweets_data


# In[222]:


tweets_df = pd.DataFrame(tweets_data,columns = ["ID","Created_at","Text","Location","UserName","UserScreenname","Userfollwerscount","Userfavouritescount","User_Description","Retweet_Count","Source","Verified_Account",
                              "User_Account_Created","Status_Count","listed_counted"])
tweets_df


# In[223]:


tweets_df.head()


# In[224]:


outfile=re.sub(r"\s+", '_', new_search)
outfile=outfile+'.csv'
print(outfile)
tweets_df.to_csv(outfile, sep=',', encoding='utf-8')


# In[225]:


tweets_df.to_csv('mbta.csv', index=False)


# In[226]:


import mysql.connector


# In[227]:


import sqlite3
conn = sqlite3.connect('neutransportation')


# In[228]:


tweets_df.to_sql('mbta',con=conn,index=False, if_exists='replace')


# In[229]:


def run_query(query):
    return pd.read_sql(query,conn)


# In[444]:


run_query('select distinct UserName,Verified_Account from mbta where Verified_Account="1"') ##To check whether Uber is a verified account or not ?


# In[445]:


run_query('select DISTINCT UserName,Userfollwerscount FROM mbta') ##To know whether how many user's are there in MBTA and their follower's


# In[446]:


run_query('select DISTINCT UserName,Userfollwerscount FROM mbta WHERE UserName = "MBTA"') ##To know whether how many followers does MBTA Has ?


# In[447]:


run_query('SELECT DISTINCT Location FROM mbta') ##From how many location mbta is getting tweets ?


# In[449]:


run_query('SELECT DISTINCT UserName,Location FROM mbta where UserName="MBTA"') ##To check from where mbta User is tweeting about MBTA


# In[452]:


run_query('select DISTINCT UserName,Source,Location from mbta where UserName="MBTA Commuter Rail"') ##To know from which Source (device) MBTA Commuter Rail user is tweeting the tweet ?


# In[453]:


run_query('SELECT DISTINCT UserName,User_Description from mbta') ##To know the user_description of the users of the MBTA to know the details ?


# In[454]:


run_query('SELECT MAX(Userfavouritescount),UserName,Text , Source , Verified_Account FROM mbta') ##To check which tweet has recieved the maximum like along with the username,Source ?


# In[455]:


run_query('SELECT  min(Userfavouritescount),UserName,Text , Source , Verified_Account FROM mbta') #To check which tweet has recieved minumun like along with the username,Source ? 


# In[461]:


run_query('SELECT COUNT(*) my_tweet_count FROM mbta LIMIT 1') #how many tweets about mbta has been tweeted ? 


# In[463]:


run_query('SELECT SUBSTR(created_at, 0, 10) tweet_date, COUNT(1) tweet_count FROM   mbta GROUP  BY SUBSTR(created_at, 0, 10) ORDER  BY COUNT(1) DESC LIMIT  5' # To check how many max tweets has been tweeted by a user on a particular day?)


# In[459]:


run_query('select distinct UserName,Status_Count from mbta where UserName="MBTA"') #To get the total no of tweets tweeted by MBTA ? 


# In[235]:


run_query('select distinct UserName,listed_counted from mbta where UserName="MBTA"') ##To get to know how many groups MBTA has Subscribed ?


# In[240]:


run_query('select distinct UserName,Location,Status_Count from mbta where location="Boston, MA" ') ## To get to know how many tweets have been issued by MBTA in Boston ?


# In[526]:


run_query('select * from mbta where Text like "%North%" ') ##To check in how many tweets the keyword North is used along with the userscreen name , followers and Description ?


# In[527]:


run_query('select * from mbta where Text like "%South%" ') ##To check in how many tweets the keyword South is used along with the userscreen name , followees and Description ?


# In[533]:


run_query('select distinct UserName ,User_Account_Created from mbta') ## When did this user join Twitter?


# In[368]:


api = tweepy.API(auth)


# In[369]:


api = tweepy.API(auth, wait_on_rate_limit=True)


username = "uber"
no_of_tweets =100


# In[370]:


try:
    tweets = api.user_timeline(screen_name=username, count=no_of_tweets)
    
    #Pulling Some attributes from the tweet
    attributes_container = [[tweet.favorite_count,tweet.source,tweet.user.name,tweet.user.followers_count,
                             tweet.text,tweet.lang,
                            tweet.id,
                             tweet.user.verified
                            ] for tweet in tweets]

    #Creation of column list to rename the columns in the dataframe
    columns = [ "Number_of_Likes", "Source","Username","followers", "Text","language","ID","Verifcation"]
    #Creation of Dataframe
    uber_df = pd.DataFrame(attributes_container, columns=columns)
except BaseException as e:
    print('Status Failed On,',str(e))
    time.sleep(3)


# In[371]:


print(uber_df)


# In[372]:


tweets_df.to_csv('uberdata.csv', index=False)


# In[373]:


api = tweepy.API(auth, wait_on_rate_limit=True)


username = "lyft"
no_of_tweets =100


# In[374]:


try:
    tweets = api.user_timeline(screen_name=username, count=no_of_tweets)
    
    #Pulling Some attributes from the tweet
    attributes_container = [[tweet.favorite_count,tweet.source,tweet.user.name,tweet.user.followers_count,
                             tweet.text,tweet.lang,
                            tweet.id,
                             tweet.user.verified
                            ] for tweet in tweets]

    #Creation of column list to rename the columns in the dataframe
    columns = [ "Number_of_Likes", "Source","Username","followers", "Text","language","ID","Verifcation"]
    #Creation of Dataframe
    lyft_df = pd.DataFrame(attributes_container, columns=columns)
except BaseException as e:
    print('Status Failed On,',str(e))
    time.sleep(3)


# In[375]:


print(lyft_df)


# In[376]:


tweets_df.to_csv('lyftdata.csv', index=False)


# In[377]:


result=pd.concat([uber_df,lyft_df], axis=0,  ignore_index=True)


# In[378]:


result_df = pd.DataFrame(result,columns = ["Number_of_Likes", "Source","Username","followers", "Text","language","ID","Verifcation"])
result_df


# In[379]:


result_df.to_csv('result.csv', index=False)


# In[510]:


import mysql.connector


# In[511]:


import sqlite3
conn = sqlite3.connect('neutransportation')


# In[512]:


result_df.to_sql('result',con=conn,index=False, if_exists='replace')


# In[513]:


def run_query(query):
    return pd.read_sql(query,conn)


# In[514]:


run_query('select distinct Username,followers from result') ##To compare the no of followers of the twitter account of uber and lyft to know their popularity ?


# In[387]:


run_query('select distinct Username,Verifcation from result where Verifcation=1') ##To Check the twitter account of uber and lyft is verified or not ?


# In[388]:


run_query('select distinct Username,Source from result') ## From which device uber and lyft are tweeting and parting their information ?


# In[394]:


run_query('select distinct language, Username from result ') #To know in which language uber and lyft are tweeting their tweets ?


# In[528]:


run_query('select Username,Text,max(Number_of_Likes) from result') ##To check among uber and lyft's tweet's which tweet have recieved the maximum likes ?


# In[520]:


run_query('select * from result where Text like "%@uber%" ') ##To assess in which tweets has the user's mentioned uber ?


# In[521]:


run_query('select count(*) from result where Text like "%@uber%" ') ##To count the number of tweets in which the user's has mentioned uber ?


# In[518]:


run_query('select * from result where Text like "%@lyft%" ') ##To assess in which tweets has the user's mentioned lyft ?


# In[522]:


run_query('select count(*) from result where Text like "%@lyft%" ') ##To count the number of tweets in which the user's has mentioned lyft ?


# In[464]:


keywords=['Uber']
print (' '.join(keywords))
num_tweets=150
print ("num_tweets ", num_tweets)


# In[465]:


new_search = "Uber -filter:retweets"


# In[466]:


# https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
# https://docs.tweepy.org/en/stable/api.html#search-tweets
tweets = tweepy.Cursor(api.search_tweets,
              q=new_search,
              lang="en",
              until=date_since).items(num_tweets)


# In[467]:


cnt=0
tweets_data = [] #initialize master list to hold our ready tweets
for tweet in tweets:
    print(cnt)    
    print(tweet)
    cnt=cnt+1


# In[468]:


# https://developer.twitter.com/en/docs/twitter-api/v1/tweets/search/api-reference/get-search-tweets
# https://docs.tweepy.org/en/stable/api.html#search-tweets
tweets = tweepy.Cursor(api.search_tweets,
              q=new_search,
              lang="en",
              until=date_since).items(num_tweets)


# In[469]:


tweets


# In[470]:


cnt=0
tweets_data = [] #initialize master list to hold our ready tweets
for tweet in tweets:
    print(cnt)    
    tweets_data.append([tweet.id_str,tweet.created_at,tweet.text.encode("utf-8"),tweet.user.location,tweet.user.name,tweet.user.screen_name,tweet.user.followers_count,tweet.user.favourites_count,tweet.user.description,tweet.retweet_count])    
    cnt=cnt+1


# In[471]:


tweets_data


# In[472]:


tweets_df = pd.DataFrame(tweets_data,columns = ["ID","Created_at","Text","Location","UserName","UserScreenname","Userfollwerscount","Userfavouritescount","User_Description","Retweet_Count"])
tweets_df 


# In[473]:


tweets_df.head()


# In[474]:


outfile=re.sub(r"\s+", '_', new_search)
outfile=outfile+'.csv'
print(outfile)
tweets_df.to_csv(outfile, sep=',', encoding='utf-8')


# In[475]:


tweets_df.to_csv('uberuser.csv', index=False)


# In[476]:


import mysql.connector


# In[477]:


import sqlite3
conn = sqlite3.connect('neutransport')


# In[478]:


tweets_df.to_sql('uberuser',con=conn,index=False, if_exists='replace')


# In[479]:


def run_query(query):
    return pd.read_sql(query,conn)


# In[494]:


run_query('SELECT SUBSTR(created_at, 0, 10) tweet_date, COUNT(1) tweet_count FROM uberuser GROUP  BY SUBSTR(created_at, 0, 10) ORDER  BY COUNT(1) DESC LIMIT  5') ##To check maximum no of tweets tweeted by uberuser on a particular day ? 


# In[498]:


run_query('select distinct(UserName),Text from uberuser') ## What user posted this tweet?


# In[496]:


run_query('SELECT UserName,Created_at FROM uber where UserName="TWA Options"')     ## When did the user post this tweet?


# In[503]:


run_query('select UserName,Text from uberuser where Created_at BETWEEN "2022-11-09" AND "2022-11-11" group by UserName') #What tweets have this user posted in the past 24 hours?


# In[502]:


run_query('select count(Created_at) ,username from uberuser where Created_at BETWEEN "2022-11-09" AND "2022-11-11" group by UserName') #How many tweets have this user posted in the past 24 hours?


# In[507]:


run_query('select UserName,Text,max(Userfavouritescount) from uberuser') #What tweets are popular?


# In[ ]:




