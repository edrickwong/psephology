from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import psycopg2
import indicoio

#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

try:
    conn = psycopg2.connect("dbname='psephology' user='twitter' host='localhost' password='twitter'")
except:
    print "I am unable to connect to the database"

cur = conn.cursor()

# consumer key, consumer secret, access token, access secret.
ckey=""
csecret=""
atoken=""
asecret=""

# Indico setup
indicoio.config.api_key = ''

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        tweet = all_data["text"]
        
        username = all_data["user"]["screen_name"] 

        print("TWEET: ")
        print(tweet)
        print("\nSENTIMENT: ")
        print(indicoio.sentiment(tweet))

        cur.execute("INSERT INTO tweets (tweet, username, sentiment) VALUES (%s,%s,%s)",
            (tweet, username, indicoio.sentiment(tweet)))

        conn.commit()

        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=['ndp'])