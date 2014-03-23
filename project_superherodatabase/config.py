from sqlalchemy.orm import scoped_session,sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Base = declarative_base()

engine = create_engine('postgresql+psycopg2://iomyonklddgwzu:9sIEO-K2EKQ8nQ5ZB64fl7s-ue@ec2-54-225-101-4.compute-1.amazonaws.com/d1n8897ubhvbft')
db_session = scoped_session(sessionmaker(autocommit=True,autoflush=True,bind=engine))
Base.query = db_session.query_property()






