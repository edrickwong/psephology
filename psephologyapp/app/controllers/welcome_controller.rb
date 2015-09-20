class WelcomeController < ApplicationController
  def index
  	ndpTweetsArray = []
  	cpcTweetsArray = []
  	lpcTweetsArray = []
  	(Date.new(2015, 9, 13)..Date.new(2015, 9, 20)).each do |date|
	  ndpTweets = Tweet.where(:tweeted_at => date.beginning_of_day..date.end_of_day).where(:party => "ndp")
	  cpcTweets = Tweet.where(:tweeted_at => date.beginning_of_day..date.end_of_day).where(:party => "cpc")
	  lpcTweets = Tweet.where(:tweeted_at => date.beginning_of_day..date.end_of_day).where(:party => "lpc")
	  ndpTweetsArray.push({:date => date, :sentiment => ndpTweets.average(:sentiment)})
	  cpcTweetsArray.push({:date => date, :sentiment => cpcTweets.average(:sentiment)})
	  lpcTweetsArray.push({:date => date, :sentiment => lpcTweets.average(:sentiment)})
	end
	gon.ndpTweets = ndpTweetsArray
	gon.cpcTweets = cpcTweetsArray
	gon.lpcTweets = lpcTweetsArray
  end
end
