# relationship with ORM
# from sqlalchemy.orm import relationship

# 建立可以直接用資料庫裡Table的格式，讓他可以自己去建立

# 變數格式的設定
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship  # 表示一個表與其他相關的表裡面的值
import datetime

Base = declarative_base()

class ProductInfo(Base):
    __tablename__ = "Product_Detail"
    tag_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    tag_name = Column(String(length=1000))
    tag_category = Column(String(length=1000))

    # com_name = relationship("ComFun", back_populates="companies")


class CompanyInfo(Base):
    __tablename__ = "Company_Detail"
    company_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(length=100))
    url = Column(String(length=1000), default=None)
    description = Column(String(length=1000), default=None)

class ComTag(Base):
    __tablename__ = "Com_Tag"
    index = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("Company_Detail.company_id"))
    tag_id = Column(Integer, ForeignKey("Product_Detail.tag_id"), index=True)
    function_id = Column(Integer, ForeignKey("Function_Detail.function_id"), index=True)



# class ComFun(Base):
#     __tablename__ = "Com_Function"
#     index = Column(Integer, primary_key=True, autoincrement=True)
#     company_id = Column(Integer, ForeignKey("Company_Detail.company_id"))
#     function_id = Column(Integer, ForeignKey("Function_Category.function_id"))

    # companies = relationship("CompanyInfo", back_populates="com_name")
    # functions = relationship("FunCat", back_populates="categories")


# class FunCat(Base):
#     __tablename__ = "Function_Category"
#     function_id = Column(Integer, primary_key=True)
#     function_name = Column(String(length=1000))
#     category_id = Column(Integer, ForeignKey("Category_Detail.category_id"))

#     # categories = relationship("ComFun", back_populates="functions")
#     # cat_id = relationship("CatInfo", back_populates="cat_name")


# class CatInfo(Base):
#     __tablename__ = "Category_Detail"
#     category_id = Column(Integer, primary_key=True, index=True)
#     category_name = Column(String(length=1000))

#     # cat_name = relationship("FunCat", back_populates="cat_id")

class TagFun(Base):
    __tablename__ = "Tag_Function"
    index = Column(Integer, primary_key=True, autoincrement=True)
    tag_id = Column(Integer, ForeignKey("Product_Detail.tag_id"))
    function_id = Column(Integer, ForeignKey("Function_Detail.function_id"), primary_key=True)


class FunInfo(Base):
    __tablename__ = "Function_Detail"
    function_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    function_name = Column(String(length=1000))