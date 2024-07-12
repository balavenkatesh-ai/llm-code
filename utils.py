from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class AwsEc2TipControl(Base):
    __tablename__ = 'aws_ec2_tip_controls'

    control_id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(String(1000))
    remediation = Column(String(1000))
    ics_std_reference_no = Column(String)
    ics_control_area = Column(String(100))
