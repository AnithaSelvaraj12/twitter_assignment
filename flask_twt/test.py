from flask import Flask, render_template, request, jsonify
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
@app.route("/home")
def home():
    return render_template("home.html")
    # return "Welcome AJ"


@app.route("/login")
def login():
    # return twitter.authorize(callback=url_for('oauth_authorized',
    # next=request.args.get('next') or request.referrer or None))
    return render_template("login.html")


@app.route("/tweets")
def get_tweets():
    # Extract the screen name from the request body
    screen_name = request.args.get("username")

    # Use Tweepy to retrieve the user's timeline tweets
    try:
        tweets = api.user_timeline(screen_name=screen_name, count=100)
    except Exception as e:
        return jsonify({" sorry the user ", screen_name, "does not exist"}), 400

    # Create a list of Tweet objects and add them to the database session
    tweet_list = []
    i = 1
    for tweet in tweets:
        print(tweet)
        tweet_obj = {"text": tweet.text, "created_at": tweet.created_at, "retweet_count": tweet.retweet_count, "favorite_count": tweet.favorite_count, "lang": tweet.lang}
        print(i)
        tweet_list.append(tweet_obj)

    # Commit the database session

    # Check if any tweets were retrieved
    if not tweet_list:
        return jsonify({"error": 'No tweets found for screen_name "{}"'.format(screen_name)}), 404

    # Return the tweet data as a JSON response
    # return jsonify({"tweets": tweet_list})
    print(tweet_list)
    return render_template("tweets.html", tweets=tweet_list)


if __name__ == "__main__":
    app.run(debug=True)
