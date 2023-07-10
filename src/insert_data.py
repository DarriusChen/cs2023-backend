from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declarative_base
from model import ComTag
from database import Base

Base = declarative_base()


Session.execute(ComTag.__table__.alter().rename_column('compnay_id', 'company_id')
)

session.commit()
session.close()
