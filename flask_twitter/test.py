from flask import Flask, render_template, request, url_for, redirect, jsonify
from models import db, Tweet, app
import os
import tweepy
import requests
import configparser as cp
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import sqlite3

basedir = os.path.abspath(os.path.dirname(__file__))


config = cp.ConfigParser()
config.read("config.ini")

auth = tweepy.OAuthHandler(eval(config["Default"]["consumer_key"]), eval(config["Default"]["consumer_secret"]))
auth.set_access_token(eval(config["Default"]["access_token"]), eval(config["Default"]["access_token_secret"]))
api = tweepy.API(auth)


@app.route("/home")
def home():
    con1 = sqlite3.connect("database.db")
    cursor = con1.execute("SELECT * FROM tweet")
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
    conn1 = sqlite3.connect("database.db")

    cursor = conn1.execute(f"SELECT * FROM tweet")
    tweets_db = cursor.fetchall()
    i = 1
    for t in tweets_db:
        if screen_name == t[1]:
            i = 0
            break
    tweet_list = []
    for tweet in tweets:
        tweet_obj = {"id": tweet.id, "text": tweet.text, "created_at": tweet.created_at, "retweet_count": tweet.retweet_count, "favorite_count": tweet.favorite_count, "lang": tweet.lang}
        print(i)
        tweet_list.append(tweet_obj)
        if i == 1:
            tweet_rec = Tweet(username=screen_name, id=tweet.id, tweet_created_at=tweet.created_at, retweet_count=tweet.retweet_count, favorite_count=tweet.favorite_count, tweet_text=tweet.text)
            db.session.add(tweet_rec)
            db.session.commit()
            print("Record_ID", tweet_rec.id)

    if not tweet_list:
        return jsonify({"error": 'No tweets found for screen_name "{}"'.format(screen_name)}), 404
    print(tweet_list)
    return render_template("tweets.html", tweets=tweet_list)


@app.route("/search")
def search_tweets():
    search = request.args.get("searchbox")
    conn1 = sqlite3.connect("database.db")
    cursor = conn1.execute(f"SELECT * FROM tweet where tweet_text LIKE '%{search}%'")
    tweets = cursor.fetchall()
    tweet_list = []
    i = 1
    for tweet in tweets:
        print(tweet)
        tweet_obj = {"text": tweet[2], "created_at": tweet[4], "retweet_count": tweet[5], "favorite_count": tweet[6], "lang": tweet[6]}
        print(i)
        tweet_list.append(tweet_obj)
    print(tweet_list)
    return render_template("tweets.html", tweets=tweet_list)


if __name__ == "__main__":
    app.run(debug=True)
