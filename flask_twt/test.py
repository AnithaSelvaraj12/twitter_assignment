from flask import Flask, render_template, request
import requests
import tweepy

app = Flask(__name__)

# Add your Twitter API keys
consumer_key = "zS2dho2nhu7ishB91yn6xpVAw"
consumer_secret = "AsUdqFbGAIT0NRFmAnz9Uf1eABlaVHZ6JujZwKeefsDg6zs4BP"
access_token = "1569658977616809984-ntKSGR8uhuKmwANNlpOsE6Hwthapkh"
access_token_secret = "c5qI44nhR3Dnc8kHhC8elTRJCfdOJEqLMaYgPD1Ek0eYi"

# Authenticate with Twitter API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Define routes for the app
@app.route("/")
def home():
    return render_template("home.html")
    # return "Welcome AJ"


@app.route("/tweets")
def tweets():
    # Add your Twitter API keys
    consumer_key = "zS2dho2nhu7ishB91yn6xpVAw"
    consumer_secret = "AsUdqFbGAIT0NRFmAnz9Uf1eABlaVHZ6JujZwKeefsDg6zs4BP"
    access_token = "1569658977616809984-ntKSGR8uhuKmwANNlpOsE6Hwthapkh"
    access_token_secret = "c5qI44nhR3Dnc8kHhC8elTRJCfdOJEqLMaYgPD1Ek0eYi"

    # Authenticate with Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    query = request.args.get("q")
    tweets = [status for status in tweepy.Cursor(api.search_tweets, q=query).items(10)]
    print(tweets)
    return render_template("tweets.html", tweets=tweets)


if __name__ == "__main__":
    app.run(debug=True)
