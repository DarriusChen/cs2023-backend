# 對資料庫進行操作
# 以fastapi的角度寫入資料庫
from typing import List
from fastapi.exceptions import HTTPException
from src import model
from sqlalchemy.orm import Session, session
from src.model import ProductInfo, CompanyInfo, ComTag
from src.schema import CompanyCreate, ProductCreate
import json

# 讀所有的資料
# def read_all_data(db: Session):
#     aa = db.query(CompanyInfo).all()
#     for row in aa:
#         print(row)


# 獲得某間公司資料(OK)
def get_company(db: Session, company_id: int):
    return db.query(CompanyInfo).filter(CompanyInfo.company_id == company_id).all()


# 獲得某個產品資料(OK)
def get_product(db: Session, tag_id: int):
    return db.query(ProductInfo).filter(ProductInfo.tag_id == tag_id).all()


# 用company_id查company細節跟存在資料庫裡的tag_id(不只一個)(OK)EX:company_id=17
def get_company_tag(db: Session, company_id: int):
    id_detail = db.query(ComTag.tag_id).filter(ComTag.company_id == company_id).all()
    id_detail = [result.tag_id for result in id_detail]
    tag_company = db.query(ProductInfo).filter(ProductInfo.tag_id.in_(id_detail)).all()
    company_detail = (
        db.query(CompanyInfo).filter(CompanyInfo.company_id == company_id).all()
    )
    new = {
        "company_id": company_detail[0].company_id,
        "name": company_detail[0].name,
        "url": company_detail[0].url,
        "description": company_detail[0].description,
        "Products": [tag.tag_name for tag in tag_company],
    }
    # for i in tag_company:
    #     company_detail[0]["tag"].update(i)

    return new
    # [i for i in tag_company]

    # "name" : company_detail.compaｃny_name,
    # "url" : company_detail.url,
    # "Description" : company_detail.description,
    # "Products" : [tag_company]


# 用tag查詢有這個Tag的所有公司id跟名稱
def get_tag_company(db: Session, tag_id: int):
    tag_id_detail = db.query(ComTag.company_id).filter(ComTag.tag_id == tag_id).all()
    tag_id_detail = [res.company_id for res in tag_id_detail]
    company_tag = (
        db.query(CompanyInfo).filter(CompanyInfo.company_id.in_(tag_id_detail)).all()
    )
    return company_tag


# category對應的tag_name
def category_tag(db: Session, category: str):
    tag_name = (
        db.query(ProductInfo.tag_name)
        .filter(ProductInfo.tag_category == category)
        .all()
    )
    return tag_name


# #獲得所有公司資料
# def read_company(db: Session, skip: int = 0, limit: int = 100):
#     return db.exec(select(CompanyInfo).offset(skip).limit(limit)).all()

# #獲得所有產品資料
# def read_product(db: Session, skip: int = 0, limit: int = 100):
#     return db.query(ProductInfo).offset(skip).limit(limit).all()


# #獲得Tag資料
# def get_product(db: Session, tag_id:Product):
#     return db.query(ProductInfo).filter(ProductInfo.tag_id == tag_id).first()


# 新增公司(OK)
def create_company(db: Session, company: CompanyCreate):
    try:
        db_company = CompanyInfo(
            company_id=company.company_id,
            name=company.name,
            url=company.url,
            description=company.description,
        )
        db.add(db_company)
        db.commit()

        db_add_companyID = ComTag(company_id=company.company_id, tag_id=company.tag_id)
        db.add(db_add_companyID)
        db.commit()
        response = True
    except Exception as e:
        print(e)
        response = False

    return response


# 新增產品Tag_name和Tag_id(OK)
def create_product(db: Session, product: ProductCreate):
    db_product = ProductInfo(
        tag_id=product.tag_id,
        tag_name=product.tag_name,
        tag_category=product.tag_category,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product
