import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

def setup_database():
    """
    Setup the database connection using environment variables.
    """
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    if not all([db_user, db_password, db_host, db_port, db_name]):
        raise ValueError("One or more database environment variables are not set.")

    db_url = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    return create_engine(db_url)

def create_session(engine):
    """
    Create a SQLAlchemy session.
    """
    Session = sessionmaker(bind=engine)
    return Session


from .setup import setup_database, Base
from .models import AwsEc2TipControl

def init_db():
    """
    Initialize the database by creating tables.
    """
    engine = setup_database()
    Base.metadata.create_all(engine)
