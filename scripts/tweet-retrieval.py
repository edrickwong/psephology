import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
import psycopg2
import indicoio
import datetime
from politicalParty import *

#!/usr/bin/python2.4
#
# Small script to show PostgreSQL and Pyscopg together
#

ndp = politicalParty("New Democratic Party", "Thomas Mulcair")
cpc = politicalParty("Conservative Party of Canada", "Stephen Harper")
lpc = politicalParty("Liberal Party of Canada", "Justin Trudeau")

ndp.keywords = ["@ndp_hq", "@thomasmulcair", "#ndp", "tom mulcair", "thomas mulcair"]
cpc.keywords = ["@cpc_hq", "@pmharper", "#cpc", "stephen harper"]
lpc.keywords = ["@liberal_party", "@justintrudeau", "#lpc", "justin trudeau"]

keywords = ndp.keywords + cpc.keywords + lpc.keywords

try:
    conn = psycopg2.connect("dbname='psephologyRails' user='twitter' host='localhost' password='twitter'")
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

        tweet = all_data["text"].lower()

        sentiment = indicoio.sentiment(tweet)

        tweeted_at = all_data["created_at"]
        
        username = all_data["user"]["screen_name"] 

        now = datetime.datetime.now()

        print("TWEET: " + tweet)

        print("USERNAME: " + username)

        print("SENTIMENT: " + str(sentiment))

        print("TWEETED_AT: " + tweeted_at)

        if any(keyword in tweet for keyword in ndp.keywords):
            cur.execute("INSERT INTO tweets (tweet, username, sentiment, tweeted_at, party, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (tweet, username, sentiment, tweeted_at, "ndp", now, now))

        if any(keyword in tweet for keyword in cpc.keywords):
            cur.execute("INSERT INTO tweets (tweet, username, sentiment, tweeted_at, party, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (tweet, username, sentiment, tweeted_at, "cpc", now, now))

        if any(keyword in tweet for keyword in lpc.keywords):
            cur.execute("INSERT INTO tweets (tweet, username, sentiment, tweeted_at, party, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s)",
            (tweet, username, sentiment, tweeted_at, "lpc", now, now))

        conn.commit()

        return(True)

    def on_error(self, status):
        print status

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# twitterStream = Stream(auth, listener())
# twitterStream.filter(track=keywords)

api = tweepy.API(auth)

date1 = datetime.date(2015, 9, 13)
date2 = datetime.date(2015, 9, 20)
day = datetime.timedelta(days=1)

searchQuery = '#ndp'  # this is what we're searching for
maxTweets = 10 # Some arbitrary large number
tweetsPerQry = 2  # this is the max the API permits

while date1 <= date2:
    # If results from a specific ID onwards are reqd, set since_id to that ID.
    # else default to no lower limit, go as far back as API allows
    sinceId = None
     
    # If results only below a specific ID are, set max_id to that ID.
    # else default to no upper limit, start from the most recent tweet matching the search query.
    max_id = -1L

    tweetCount = 0

    nextDate = date1 + day

    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry, since=date1, until=nextDate)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId, since=date1, until=nextDate)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1), since=date1, until=nextDate)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId, since=date1, until=nextDate)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweetData in new_tweets:

                tweet = tweetData.text

                sentiment = indicoio.sentiment(tweet)

                tweeted_at = tweetData.created_at

                now = datetime.datetime.now()

                print("TWEET: " + tweet)

                print("SENTIMENT: " + str(sentiment))

                print("TWEETED_AT: " + str(tweeted_at))

                if any(keyword in tweet for keyword in ndp.keywords):
                    cur.execute("INSERT INTO tweets (tweet, sentiment, tweeted_at, party, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s)",
                    (tweet, sentiment, tweeted_at, "ndp", now, now))

                if any(keyword in tweet for keyword in cpc.keywords):
                    cur.execute("INSERT INTO tweets (tweet, sentiment, tweeted_at, party, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s)",
                    (tweet, sentiment, tweeted_at, "cpc", now, now))

                if any(keyword in tweet for keyword in lpc.keywords):
                    cur.execute("INSERT INTO tweets (tweet, sentiment, tweeted_at, party, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s)",
                    (tweet, sentiment, tweeted_at, "lpc", now, now))

                conn.commit()

            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:
            # Just exit if any error
            print("some error : " + str(e))
            break


    date1 = date1 + day

    


