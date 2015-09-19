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
ckey="WE2891N5RET0JJw1CYOOKZyHY"
csecret="0B6RwoWUfoKuyA8sn1Z3vkLdNu1b58Sh2a3O9skpqRc2TnD90c"
atoken="2254230432-pajLITCj09mYcK7goVIeZobpfGrxcbPc0jqUXy5"
asecret="QMwW4NS4TQqb5SXov7Rby8wbkX559isDgzxFgt9LzUeg0"

# Indico setup
indicoio.config.api_key = '6f6cfb806632d4b45101a5b7db77fc29'

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)

        tweet = all_data["text"]

        sentiment = indicoio.sentiment(tweet)

        tweeted_at = all_data["created_at"]
        
        username = all_data["user"]["screen_name"] 

        print("TWEET: " + tweet)

        print("USERNAME: " + username)

        print("SENTIMENT: " + str(sentiment))

        print("TWEETED_AT: " + tweeted_at)

        cur.execute("INSERT INTO tweets (tweet, username, sentiment, tweeted_at) VALUES (%s,%s,%s,%s)",
            (tweet, username, sentiment, tweeted_at))

        conn.commit()

        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=['ndp'])