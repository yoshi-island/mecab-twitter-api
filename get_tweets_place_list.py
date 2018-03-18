#!/usr/bin/env python
# -*- coding:utf-8 -*-
# python 3.5.0


###################
# usage
###################
#
#user = "<tweetuser>"
#place_list_rank = get_tweets_place_list(user)
#
# passwords.py
# oath_keys = {
#  "consumer_key": "",
#  "consumer_secret": "",
#  "access_token": "",
#  "access_token_secret": ""
#  }


###################
# import modules
###################

from requests_oauthlib import OAuth1Session
import json
import MeCab
import collections
import passwords

###################
# variables
###################

oath_keys = passwords.oath_keys



###################
# create oath session
###################
def session_create(oath_keys):
  oath = OAuth1Session(
  oath_keys["consumer_key"],
  oath_keys["consumer_secret"],
  oath_keys["access_token"],
  oath_keys["access_token_secret"]
  )
  return oath



###################
# get tweets
###################
def get_tweets(user,oath):
  user = user
  url = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
  params = {
    "screen_name": user,
    "count": "1000"
    }
  oath = oath
  responce = oath.get(url, params = params)

  if responce.status_code != 200:
    print("Error code: %d" %(responce.status_code))
    return None
  tweets = json.loads(responce.text)
  #tweets_format = json.dumps(tweets, indent=4, separators=(',', ': '))
  #print(tweets_format)

  tweets_text_list = ""
  for l in tweets:
    tweets_text_list += l['text'] + "\n"

  return tweets_text_list



###################
# mecab_analyze_tweets
###################
def mecab_analyze_tweets(tweets_text_list):
  tweets_text_list = tweets_text_list.split("\n")
  mecab = MeCab.Tagger("-Ochasen")
  place_list = []
  place_list_srctwt = []
  for l in tweets_text_list:
    if len(l) > 0:
      mecab_parsed = mecab.parse(l)
      items = mecab_parsed.split("\t")
      if len(items)>4:
        if items[3].find("地域") > -1:
          if len(items[0]) > 1:
            if items[0] != "日本":
              place_list.append(items[0])
              place_list_srctwt.append(l)

  count_dict = collections.Counter(place_list)  
  place_list_rank = count_dict.most_common(10)

  return place_list_rank,place_list_srctwt



###################
# main
###################
#if __name__ == "__main__":
def get_tweets_place_list(user):
  oath = session_create(oath_keys)
  tweets_text_list = get_tweets(user,oath) # list
  place_list_rank,place_list_srctwt = mecab_analyze_tweets(tweets_text_list) # list
  return place_list_rank, place_list_srctwt
