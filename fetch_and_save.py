#encoding:'utf-8'
import tweepy
import json
from tweepy.streaming import StreamListener
from tweepy import Stream

#https://developer.twitter.com/en/apps/15864485
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

save_file = open('raw_tweets.json','a')


class StdOutListener(StreamListener):

    def on_data(self, data):
        json_data = json.loads(data)
        if "delete" not in json_data: #  first level keys
            save_file.write(data)
            print(data)
        return True

    def on_error(self, status):
        print('Encountered error with status code:', status_code)       
        # If the error code is 401, which is the error for bad credentials
        if status_code == 401:
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
        time.sleep(10)        
        return

stream = Stream(auth, StdOutListener())
# set parameter language, location  
# https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/basic-stream-parameters
stream.filter(languages=['en'],track=['the','i','to','a','and','is','in','it','you','of'])
# stream.sample() # no filter
