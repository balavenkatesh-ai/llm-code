from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class TimestampMixin:
    @declared_attr
    def created_by(cls):
        return Column(String, nullable=False)

    @declared_attr
    def modified_by(cls):
        return Column(String, nullable=True)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def modified_at(cls):
        return Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    
    
