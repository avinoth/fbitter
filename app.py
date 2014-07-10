from flask import Flask, redirect, url_for, session, request, render_template, flash
from flask_oauth import OAuth
from flask.ext.tweepy import Tweepy

app = Flask(__name__)
app.config.from_object('config')
oauth = OAuth()
consumer_key = app.config["CONSUMER_ID"]
consumer_secret = app.config["CONSUMER_SECRET"]
access_token_key = app.config["ACCESS_KEY"]
access_token_secret = app.config["ACCESS_SECRET"]


twitter = oauth.remote_app('twitter',
    base_url='https://api.twitter.com/1/',
    request_token_url='https://api.twitter.com/oauth/request_token',
    access_token_url='https://api.twitter.com/oauth/access_token',
    authorize_url='https://api.twitter.com/oauth/authenticate',
    consumer_key=consumer_key,
    consumer_secret=consumer_secret
)

@app.route('/')
def home():
    return render_template('index.html')


@twitter.tokengetter
def get_twitter_token(token=None):
    return session.get('twitter_token')



@app.route('/login')
def login():
    return twitter.authorize(callback=url_for('oauth_authorized',
                                next=request.args.get('next') or request.referrer or None))
    
    
@app.route('/oauth-authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
    next_url = request.args.get('next') or url_for('index')
    if resp is None:
        flash(u'Access has been denied for the application.')
        return redirect(next_url)

    session['twitter_token'] = (
        resp['oauth_token'],
        resp['oauth_token_secret']
    )

    session['twitter_user'] = resp['screen_name']

    flash('Welcome, %s' % resp['screen_name'])
    return redirect(next_url)



@app.route('/timeline')
def index():
    resp = twitter.get('statuses/home_timeline.json')
    if resp.status == 200:
        tweets = resp.data
    else:
        tweets = None
        flash(resp)
        flash(resp.status)
    return render_template('index.html', tweets=tweets)  




if __name__ == '__main__':
    app.run()
    