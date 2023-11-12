# ### CREATE A DB ###

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///originallyverified/originallyverified.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Twitnits(Base):
    """ Describe the twits table """
    __tablename__ = 'twitnits'
    """
    {
        'id': 'Primary Key',
        'user_created_at': 'DATETIME', 
        'verified': 'BOOLEAN', 
        'twitter_id': 'String',
        'username': 'String',
        'name': 'String',
        'wallet_address': 'String',
        'profile_image_url': 'String',
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
        }


def make_session():
    engine = create_engine('sqlite:///originallyverified/originallyverified.db')
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
