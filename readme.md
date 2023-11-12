# Verified Twitters

Just a script that uses tweepy to grab all verified users and put them in a DB for future use.

***Update: added user metrics in new extended DB***

### Setup

copy and edit `env-example` to `.env`

Source it

`source .env`

Create a virtualenv

`virtualenv -p python3 venv`

Source it

`source venv/bin/activate`

Install requirements

`pip install -r requirements.txt`

Create the local sqlite DB

`python db_models.py`

### Run It

`python get_verified_users.py`

Go get coffee, lots of coffee


### Ref Links

https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

https://dev.to/twitterdev/a-comprehensive-guide-for-using-the-twitter-api-v2-using-tweepy-in-python-15d9

https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_followers


