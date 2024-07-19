from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from datetime import datetime

@as_declarative()
class Base:
    id: int = Column(Integer, primary_key=True, index=True)
    created_by: str = Column(String, nullable=True)
    created_at: datetime = Column(DateTime, default=datetime.utcnow)
    updated_by: str = Column(String, nullable=True)
    updated_at: datetime = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)




from sqlalchemy import Column, String, Integer, JSON, create_engine
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

Base = declarative_base()

class FirewallPolicyRequests(Base):
    __tablename__ = 'firewall_policy_requests'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(PG_UUID(as_uuid=True), default=uuid.uuid4, nullable=False)
    request = Column(JSON, nullable=False)
    status = Column(String, nullable=False)
    response = Column(JSON, nullable=True)
    response_status_code = Column(Integer, nullable=True)
    business_application_details = Column(JSON, nullable=False)
    policy_engine_response = Column(JSON, nullable=False)
    policy_evaluation_status = Column(String, nullable=False)
    policy_version = Column(String, nullable=False)

# Database setup (replace with your database URL)
DATABASE_URL = "postgresql+psycopg2://user:password@localhost/dbname"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)