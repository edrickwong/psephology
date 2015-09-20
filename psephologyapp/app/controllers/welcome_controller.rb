class WelcomeController < ApplicationController
  def index
  	ndpTweetsArray = []
  	cpcTweetsArray = []
  	lpcTweetsArray = []

  	ndpSentiment = []
  	cpcSentiment = []
  	lpcSentiment = []
  	dates = []
  	(Date.new(2015, 9, 13)..Date.new(2015, 9, 20)).each do |date|
	  ndpTweets = Tweet.where(:tweeted_at => date.beginning_of_day..date.end_of_day).where(:party => "ndp")
	  cpcTweets = Tweet.where(:tweeted_at => date.beginning_of_day..date.end_of_day).where(:party => "cpc")
	  lpcTweets = Tweet.where(:tweeted_at => date.beginning_of_day..date.end_of_day).where(:party => "lpc")
	  ndpSentiment.push(ndpTweets.average(:sentiment))
	  cpcSentiment.push(cpcTweets.average(:sentiment))
	  lpcSentiment.push(lpcTweets.average(:sentiment))
	  dates.push(date)
	end
	gon.ndpSentiment = ndpSentiment
	gon.cpcSentiment = cpcSentiment
	gon.lpcSentiment = lpcSentiment
	gon.dates = dates
  end
end
