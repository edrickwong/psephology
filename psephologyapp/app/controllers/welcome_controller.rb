class WelcomeController < ApplicationController
  def index
  	gon.tweets = Tweet.limit(10)
  end
end
