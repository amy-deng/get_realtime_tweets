#encoding:'utf-8'
import tweepy
import json
import sys
import time
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

file_name = time.strftime('%Y-%m-%d', time.localtime())
save_file = open('crime/'+file_name+'.json','a')


class StdOutListener(StreamListener):

    def __init__(self, start_time, time_limit=60):
        self.time = start_time
        self.limit = time_limit

    def on_data(self, data):
        if (time.time()-self.time) < self.limit:
            json_data = json.loads(data)
            if "delete" not in json_data: #  first level keys
                print(data[:71])
                save_file.write(data)
            return True
        
        return False
        

    def on_error(self, status):
        if (time.time()-self.time) >= self.limit:
            print('Time is over')
            return False
        else:
            # If the error code is 401, which is the error for bad credentials
            print('Encountered error with status code:', status)
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


stream = Stream(auth, StdOutListener(time.time(),5600))
file = open('words_one_word_one_line.txt').read() # or "a+", whatever you need
words = file.split("\n") # check last one which might be '' in some version of python
while True:
    try:
      stream.filter(languages=['en'], track=words, stall_warnings=True)
    except ProtocolError:
        continue
