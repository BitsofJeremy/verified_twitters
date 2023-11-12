# ### CREATE A DB ###

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///originallyverified_extended.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class OriginallyVerified(Base):
    """ Describe the twits table """
    __tablename__ = 'originallyverified'
    """
    {
        'id': 'Primary Key',
        'user_created_at': 'DATETIME', 
        'verified': 'BOOLEAN', 
        'twitter_id': 'String',
        'username': 'String',
        'name': 'String',
        'profile_image_url': 'String',
        'followers_count': 'Integer',
        'following_count': 'Integer',
        'tweet_count': 'Integer',
        'listed_count': 'Integer' 
    }
    """
    id = Column(Integer, primary_key=True)
    user_created_at = Column(DateTime)
    verified = Column(Boolean)
    twitter_id = Column(String())
    username = Column(String())
    name = Column(String())
    wallet_address = Column(String())
    profile_image_url = Column(String())

    # Extended data
    followers_count = Column(Integer())
    following_count = Column(Integer())
    tweet_count = Column(Integer())
    listed_count = Column(Integer())

    def __init__(self, twitter_id, username):
        self.twitter_id = twitter_id
        self.username = username

    def __repr__(self):
        return f"{self.twitter_id}-{self.username}"

    def update(self, **kwargs):
        """ Updates a task information  """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def serialize(self):
        """ Returns a dictionary of the twitnit information """
        return {
            'id': self.id,
            'user_created_at': self.user_created_at,
            'verified': self.verified,
            'twitter_id': self.twitter_id,
            'username': self.username,
            'name': self.name,
            'wallet_address': self.wallet_address,
            'profile_image_url': self.profile_image_url,
            'followers_count': self.followers_count,
            'following_count': self.following_count,
            'tweet_count': self.tweet_count,
            'listed_count': self.listed_count,
        }


def make_extended_session():
    engine = create_engine('sqlite:///originallyverified_extended.db')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def main():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()
    session.close()
    print("Created DB")


if __name__ == '__main__':
    main()
