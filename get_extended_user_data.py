# Ensures the API keys are correct
import datetime
import os
import tweepy
# original DB snapshot from Friday 11/05/2022 @ 645am
from db_models import make_session, Twitnits
# New DB with extended metrics
from db_models_extended import make_extended_session, OriginallyVerified

# Twitter API credentials
CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
# Setup a client for the pagination
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
    wait_on_rate_limit=True
)

# Create session with the original DB
session = make_session()
# Create an extended DB session
extended_session = make_extended_session()
# Pull all originallyverified users from DB
# There are a bunch of folks in the original DB
# that actually were not verified according to the twitter API.
# Removing those user accounts to make a more pure dataset
ov_users = session.query(Twitnits).filter(Twitnits.verified == True).all()

# Do it
try:
    for user in ov_users:
        # Each record has a serialize function to export data nicely
        user_info = user.serialize
        # Actually get the user data from the Twitter API
        # note: the extra data pulled from public_metrics
        res = client.get_user(
            id=user_info['twitter_id'],
            user_fields=[
                'public_metrics',
            ]
        )
        # print(res)
        # print(res.data.public_metrics)

        # FIX:
        # AttributeError: 'NoneType' object has no attribute 'public_metrics'
        try:
            public_metrics = res.data.public_metrics
        except AttributeError:
            # User has no public_metrics for some reason?!?
            print(f"User {user_info['username']} has no public_metrics for some reason?!?")
            public_metrics = {
                'followers_count': 0,
                'following_count': 0,
                'tweet_count': 0,
                'listed_count': 0
            }
        # print(user_info)
        extended_user_data = {
            'user_created_at': user_info['user_created_at'],
            'verified': user_info['verified'],
            'twitter_id': user_info['twitter_id'],
            'username': user_info['username'],
            'name': user_info['name'],
            'wallet_address': '0x00000000',
            'profile_image_url': user_info['profile_image_url'],
            'followers_count': public_metrics['followers_count'],
            'following_count': public_metrics['following_count'],
            'tweet_count': public_metrics['tweet_count'],
            'listed_count': public_metrics['listed_count']
        }
        # print(user_data)
        # Create user in extended DB
        extended_user = OriginallyVerified(
            twitter_id=user_info['twitter_id'],
            username=user_info['username']
        )
        # Add the rest of the data by unpacking
        extended_user.update(**extended_user_data)
        # Write it out to the DB
        extended_session.add(extended_user)
        extended_session.commit()
finally:
    print("Finished")
