import json
import time
import atexit
import tweepy
from flask import Flask
from os import environ as env
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv(dotenv_path='.env')

local_woeid = env.get('DEFAULT_WOEID')
auth = tweepy.OAuthHandler(env.get('API_KEY'), env.get('API_SECRET_KEY'))
auth.set_access_token(env.get('ACCESS_TOKEN'),
                      env.get('ACCESS_TOKEN_SECRET'))
api = tweepy.API(auth)
app = Flask(__name__)
mentions = []


def process_mention(data):
    pass


# Listen to user's mentions every 5 minutes
def listen_mentions():
    request = api.mentions_timeline()
    for mention in request:
        if not(mention.id in mentions):
            mentions.append(mention.id)
            process_mention('test')
            break
    if(len(mentions) == 20):
        i = 1
        while(mentions[-i] != request[-i].id):
            i += 1
        del mentions[-i:]
    # print(request)


def snake_trends(woeid=local_woeid):
    request = api.trends_place(id=woeid)[0]
    trends = request['trends']
    locations = request['locations']


@app.route('/')
def root():
    return 'Hello, world! I am Snakey Bot 🐍'


scheduler = BackgroundScheduler()
scheduler.add_job(func=listen_mentions, trigger="interval", seconds=5)
# scheduler.add_job(func=retrieve_trends, trigger="interval", seconds=5)
scheduler.start()

# # Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
