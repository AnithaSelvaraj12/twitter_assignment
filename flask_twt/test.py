from flask import Flask, render_template, request, url_for, redirect, jsonify
from models import db, Tweet
import os
import tweepy
import requests
import configparser as cp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import sqlite3

conn = sqlite3.connect("database.db")


basedir = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy()


def app_obj():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "database.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_RECORD_QUERIES"] = True
    db.init_app(app)

    @app.before_first_request
    def create_database():
        db.create_all()

    try:
        db.create_all()
    except Exception as exception:
        print("got the following exception when attempting db.create_all() in __init__.py: " + str(exception))
    finally:
        print("db.create_all() in __init__.py was successfull - no exceptions were raised")

    return app


app = app_obj()


config = cp.ConfigParser()
config.read("config.ini")

auth = tweepy.OAuthHandler(eval(config["Default"]["consumer_key"]), eval(config["Default"]["consumer_secret"]))
auth.set_access_token(eval(config["Default"]["access_token"]), eval(config["Default"]["access_token_secret"]))
api = tweepy.API(auth)

# Define routes for the app
@app.route("/home")
def home():
    cursor = conn.execute("SELECT * FROM tweet")
    rows = cursor.fetchall()
    return render_template("tweets.html", tweets=rows)


@app.route("/login")
def login():

    return render_template("login.html")


@app.route("/tweets")
def get_tweets():
    screen_name = request.args.get("username")

    try:
        tweets = api.user_timeline(screen_name=screen_name, count=100)
    except Exception as e:
        return jsonify({" sorry the user ", screen_name, "does not exist"}), 400

    tweet_list = []
    i = 1
    for tweet in tweets:
        print(tweet)
        tweet_obj = {"text": tweet.text, "created_at": tweet.created_at, "retweet_count": tweet.retweet_count, "favorite_count": tweet.favorite_count, "lang": tweet.lang}
        print(i)
        tweet_list.append(tweet_obj)
        tweet_rec = Tweet(username=screen_name, tweet_created_at=tweet.created_at, retweet_count=tweet.retweet_count, favorite_count=tweet.favorite_count, tweet_text=tweet.text)
        db.session.add(tweet_rec)
        db.session.commit()
        print("Record_ID", tweet_rec.id)

    if not tweet_list:
        return jsonify({"error": 'No tweets found for screen_name "{}"'.format(screen_name)}), 404
    print(tweet_list)
    return render_template("tweets.html", tweets=tweet_list)


if __name__ == "__main__":
    app.run(debug=True)
