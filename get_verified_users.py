# Ensures the API keys are correct
import os
import tweepy
from db_models import make_session, Twitnits

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
# Account ID for @verified https://twitter.com/verified/following
account_id = 63796828
# Create session in DB
session = make_session()
# Do it
try:
    # 1000 is the largest number allowed
    for response in tweepy.Paginator(
            client.get_users_following,
            account_id,
            user_fields=[
                'created_at',
                'verified',
                'profile_image_url'
            ],
            max_results=1000):
        # Rip through the users to get their info.
        for user in response.data:
            user_data = {
                'user_created_at': user.created_at,
                'verified': user.verified,
                'twitter_id': str(user.id),
                'username': user.username,
                'name': user.name,
                'wallet_address': '0x00000000',
                'profile_image_url': user.profile_image_url,
            }
            # print(user_data)
            # Create user in DB
            t = Twitnits(
                twitter_id=str(user.id),
                username=user.username
            )
            # Add the rest of the data by unpacking
            t.update(**user_data)
            # Write it out to the DB
            session.add(t)
            session.commit()
finally:
    print("Finished")
