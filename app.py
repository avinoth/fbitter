from flask import Flask, redirect, url_for, session, request, render_template, flash
import tweepy
import flask

app = Flask(__name__)
app.config.from_object('config')
consumer_key = app.config["CONSUMER_ID"]
consumer_secret = app.config["CONSUMER_SECRET"]
access_token_key = app.config["ACCESS_KEY"]
access_token_secret = app.config["ACCESS_SECRET"]

@app.route('/')
def send_token():
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret)
    api = tweepy.API(auth)
    return flask.render_template('tweets.html', tweets=api.user_timeline())


if __name__ == '__main__':
    app.run()