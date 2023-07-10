
# create model attribute/column
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float

# relationship with ORM
#from sqlalchemy.orm import relationship

#建立可以直接用資料庫裡Table的格式，讓他可以自己去建立

#變數格式的設定
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from src.database import Base#從database導入Base繼承
from sqlalchemy.orm import relationship#表示一個表與其他相關的表裡面的值
import datetime


class ProductInfo(Base):
    __tablename__ = "Product_Detail"
    tag_id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(length=100))

class CompanyInfo(Base):
    __tablename__ = "Company_Detail"
    company_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=100))
    url = Column(String(length = 100), default = None)
    description = Column(String(length = 1000), default = None)
    
    
class ComTag(Base):
    __tablename__ = "Com_Tag"
    index = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("Company_Detail.company_id"))
    tag_id = Column(Integer, ForeignKey("Product_Detail.tag_id"))
    