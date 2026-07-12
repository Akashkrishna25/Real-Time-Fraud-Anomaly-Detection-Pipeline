# from sqlalchemy import Column, Integer, Float
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

# class Transaction(Base):

#     __tablename__ = "transactions"

#     id = Column(Integer, primary_key=True, index=True)

#     amount = Column(Float)
#     prediction = Column(Integer)

from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Transaction(Base):

    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer)

    merchant = Column(String)

    country = Column(String)

    payment_method = Column(String)

    device = Column(String)

    amount = Column(Float)

    risk_score = Column(Integer)

    prediction = Column(Integer)