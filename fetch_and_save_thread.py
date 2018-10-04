import tweepy
import json
import sys,os
import time,datetime
from threading import Thread
from tweepy.streaming import StreamListener
from tweepy import Stream
from urllib3.exceptions import ProtocolError

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_proper_file(key_type):
    cur_time = time.strftime('%Y-%m-%d', time.localtime())
    return open(key_type+'/'+cur_time+'.json','a')

class StdOutListener(StreamListener):

    def __init__(self,key_type):
        self.save_file = get_proper_file(key_type)
        

    def on_data(self, data):
        now = datetime.datetime.now()
        today8am = now.replace(hour=8, minute=0, second=0)
        today24pm = now.replace(hour=23, minute=59, second=0)
        if now > today8am and now < today24pm:
            json_data = json.loads(data)
            if "delete" not in json_data: #  first level keys
                print(data[:71])
                self.save_file.write(data)
            return True
        
        print("Evening time")
        time.sleep(60)
        return False
        

    def on_error(self, status):
        # If the error code is 401, which is the error for bad credentials
        print('Encountered error with status code:', status)
        return False

    # When a deleted tweet appears
    def on_delete(self):        
        print("Delete notice")
        return

    # When reach the rate limit
    def on_limit(self, track):        
        print("Rate limited, continuing")        
        return True
    
    def on_timeout(self):
        print(sys.stderr, 'Timeout...')        
        # time.sleep(10)        
        return 
    def om_exception(self, exception):
        print(exception)
        return

def get_tweets(key_type):
    print(key_type,' start fetching')
    stream = Stream(auth, StdOutListener(key_type))
    file = open('words_about_'+key_type+'.txt').read()
    words = file.split("\n")
    stream.filter(languages=['en'], track=words, stall_warnings=True,async=True)
    time.sleep(5)

if __name__ == '__main__':
    while True:
        try:
            Thread(target = get_tweets('health')).start()
            Thread(target = get_tweets('crime')).start()
        except ProtocolError:
            continue
