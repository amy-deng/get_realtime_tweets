#encoding:'utf-8'
import tweepy
import json
import sys
import time
from tweepy.streaming import StreamListener
from tweepy import Stream

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

save_file = open('raw_tweets.json','a')


class StdOutListener(StreamListener):

    def __init__(self, start_time, time_limit=60):
        self.time = start_time
        self.limit = time_limit

    def on_data(self, data):
        if (time.time()-self.time) < self.limit:
            json_data = json.loads(data)
            if "delete" not in json_data: #  first level keys
                print(data)
                save_file.write(data)
            return True
        
        return False
        

    def on_error(self, status):
        if (time.time()-self.time) >= self.limit:
            print('Time is over')
            return False
        elif status == 401:
            # If the error code is 401, which is the error for bad credentials
            print('Encountered error with status code:', status_code)
            return False

    # When a deleted tweet appears
    def on_delete(self, status_id, user_id):        
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

stream = Stream(auth, StdOutListener(time.time(),3600))
# parameter language, location ????
stream.filter(languages=['en'],track=['the','i','to','a','and','is','in','it','you','of'])
# stream.sample()
