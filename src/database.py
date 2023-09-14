from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2


conn = psycopg2.connect(
    dbname='postgres',
    user='admin',
    host='db',
    password='admin'
)


engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base = declarative_base()