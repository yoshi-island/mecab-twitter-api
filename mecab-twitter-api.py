#!/usr/bin/env python
# -*- coding:utf-8 -*-
# python 3.5.0


###################
# import modules
###################

import get_tweets_place_list
from flask import Flask, jsonify, abort, make_response
import netifaces
import json



#place_list_rank = get_tweets_place_list.get_tweets_place_list("@r_otake0818")
#[('日本', 30), ('北朝鮮', 3), ('韓国', 3), ('梅田', 2), ('中国', 2), ('大阪', 2), ('朝鮮', 2), ('ウクライナ', 2), ('アメリカ', 1), ('ブラジル', 1)]


###################
# get local address
###################

sv_ip = netifaces.ifaddresses('eth0')[netifaces.AF_INET][0]['addr']

###################
# api functions
###################

api = Flask(__name__)
api.config['JSON_AS_ASCII'] = False # for Japanese language

@api.route('/getTweetsPlace/<string:userId>', methods=['GET'])
def get_user(userId):
  user = userId

  try:
    place_list_rank = get_tweets_place_list.get_tweets_place_list(user) # error judge
    place_name = place_list_rank[0][0] # data existance judge
    place_cnt = place_list_rank[0][1] # data existance judge
  except:
    return make_response(jsonify({'error': 'Not found'}), 404)

  rank_list = [
    {
      "number": 1,
      "place": place_name,
      "count": place_cnt
    }]

  for i in range (1,5):
    place_name = ""
    place_cnt = ""
    try: 
      place_name = place_list_rank[i][0]
      place_cnt  = place_list_rank[i][1]
      component = {
          "number": i,
          "place": place_name,
          "count": place_cnt
        }
      rank_list.append(component)
    except:
      break

  result = {
    "result":True,
    "data":{
      "userId":user,
      "rank":rank_list 
    }
  }

  return make_response(jsonify(result))


@api.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

if __name__ == '__main__':
    api.run(host=sv_ip, port=3000)
