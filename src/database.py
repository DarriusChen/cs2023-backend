from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src import model

SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@0.0.0.0/postgres"

# create SQL engine
#直接連到SQL Alchemy的database的url
#啟動Engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)



# create SQL communication session and bind
#啟動Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create SQL mapping table
Base = declarative_base()