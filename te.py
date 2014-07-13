from flask import Flask, redirect, url_for, session, request, render_template, flash
import tweepy
import flask

app = Flask(__name__)
app.config.from_object('config')
consumer_key = app.config["CONSUMER_ID"]
consumer_secret = app.config["CONSUMER_SECRET"]
access_token_key = app.config["ACCESS_KEY"]
access_token_secret = app.config["ACCESS_SECRET"]

callback_url = 'http://localhost:5000/verify'
session = dict()

@app.route('/')
def send_token():
    redirect_url = ""
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, callback_url)
    #get the request tokens
    try: 
        redirect_url = auth.get_authorization_url()
    except tweepy.TweepError:
        print 'Error! Failed to get request token'
    return flask.redirect(redirect_url)

@app.route("/verify")
def get_verification():
    #get the verifier key from the request url
    verifier = request.args['oauth_verifier']
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token_key, access_token_secret) 
    try:
        auth.get_access_token(verifier)
    except tweepy.TweepError:
        print 'Error! Failed to get access token.'

    api = tweepy.API(auth)
    return flask.render_template('tweets.html', tweets=api.user_timeline())

if __name__ == '__main__':
    app.run()
    
