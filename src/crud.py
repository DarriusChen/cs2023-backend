# 對資料庫進行操作
# 以fastapi的角度寫入資料庫
from typing import List
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from src.model import ProductInfo, CompanyInfo, ComTag, FunInfo
from src.schema import CompanyCreate, ProductCreate, NewCompany, AllNewCompany, CompareCompany
import json


# 獲得某間公司資料(OK)
def get_company(db: Session, cid: int):
    id_detail = [i.tag_id for i in db.query(ComTag.tag_id).filter(ComTag.company_id == cid).all()]
    tag_company = db.query(ProductInfo).filter(ProductInfo.tag_id.in_(id_detail)).all()
    company_detail = db.query(CompanyInfo).filter(CompanyInfo.company_id == cid).all()
    return {
        "company_id":company_detail[0].company_id,
        "name": company_detail[0].name,
        "url": company_detail[0].url,
        "description": company_detail[0].description,
        "Products": [tag.tag_name for tag in tag_company],
    }


# 獲得某個產品資料(OK)
def get_product(db: Session, tag_id: int):
    return db.query(ProductInfo).filter(ProductInfo.tag_id == tag_id).all()


# 用company_id查company細節跟存在資料庫裡的tag_id(不只一個)(OK)
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
    return new


# 用tag查詢有這個Tag的所有公司id跟名稱
def get_tag_company(db: Session, tag_id: int):
    tag_id_detail = db.query(ComTag.company_id).filter(ComTag.tag_id == tag_id).all()
    tag_id_detail = [res.company_id for res in tag_id_detail]
    company_tag = (
        db.query(CompanyInfo).filter(CompanyInfo.company_id.in_(tag_id_detail)).all()
    )
    return company_tag


# category對應的tag_name
def category_tag(db: Session):
    category_name = db.query(ProductInfo.tag_category).distinct().all()
    c_names = [t[0] for t in category_name]
    c_new_list = []
    for res in c_names:
        c_tag_name = (
            db.query(ProductInfo.tag_name).filter(ProductInfo.tag_category == res).distinct().all()
        )
        new_category = {res: list(set(i.tag_name for i in c_tag_name))}
        c_new_list.append(new_category)
    return c_new_list


# 獲得所有公司資料
def read_company(db: Session):
    company_ID = db.query(CompanyInfo.company_id).all()
    numbers = [t[0] for t in company_ID]
    new_list = []
    for res in numbers:
        id_detail = db.query(ComTag.tag_id).filter(ComTag.company_id == res).all()
        id_detail = [result.tag_id for result in id_detail]
        tag_company = (
            db.query(ProductInfo).filter(ProductInfo.tag_id.in_(id_detail)).all()
        )
        company_detail = (
            db.query(CompanyInfo).filter(CompanyInfo.company_id == res).all()
        )
        new_all = {
            "company_id": company_detail[0].company_id,
            "name": company_detail[0].name,
            "url": company_detail[0].url,
            "description": company_detail[0].description,
            "Products": [tag.tag_name for tag in tag_company],
        }
        new_list.append(new_all)
    return new_list


# read_all_company = db.query(CompanyInfo).all()


# 獲得所有產品資料
def read_product(db: Session):
    read_all_product = db.query(ProductInfo).all()


# 新增公司的內容(OK)
def create_company(db: Session, company: CompanyCreate):
    try:
        db_company = CompanyInfo(
            #company_id=company.company_id,
            name=company.name,
            url=company.url,
            description=company.description,
        )
        db.add(db_company)
        db.commit()

        for tag_id in company.tag_id:  # Iterate through tag_ids
            db_add_companyID = ComTag(company_id=db_company.company_id, tag_id=tag_id)
            db.add(db_add_companyID)
        db.commit()
        response = True
    except Exception as e:
        print(e)
        response = False

    return response


# 新增產品的所有相關資訊(OK)
def create_product(db: Session, product: ProductCreate):
    db_product = ProductInfo(
        tag_name=product.tag_name,
        tag_category=product.tag_category,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# 公司的category對應到有的產品
def company_function(db: Session, company_id: int):
    id_detail = db.query(ComTag).filter(ComTag.company_id == company_id).all()
    id_detail = [result.tag_id for result in id_detail]
    tag_company = db.query(ProductInfo).filter(ProductInfo.tag_id.in_(id_detail)).all()
    comtag_id = [tag.tag_id for tag in tag_company]
    
    tag_fun_records = db.query(TagFun).filter(TagFun.tag_id.in_(comtag_id)).all()
    tag_id_function_id_pairs = [(record.tag_id, record.function_id) for record in tag_fun_records]

    last = []
    company_detail = (
        db.query(CompanyInfo).filter(CompanyInfo.company_id == company_id).all()
    )
    last = {
        "company_id": company_detail[0].company_id,
        "name": company_detail[0].name,
        "Products_Detail": [tag.tag_name for tag in tag_company],
    }
    return tag_fun_records


#刪除整間公司的所有相關內容
def delete_company(db: Session, company_id: int):
    try:
        # 刪除引用紀錄（ComTag 表中的紀錄）
        db.query(ComTag).filter(ComTag.company_id == company_id).delete(synchronize_session=False)
        
        # 刪除主表紀錄（CompanyInfo 表中的紀錄）
        db.query(CompanyInfo).filter(CompanyInfo.company_id == company_id).delete(synchronize_session=False)

        db.commit()
        response = True
    except Exception as e:
        print(e)
        db.rollback()  
        response = False
    return response    

# #更新公司資訊
def update_company(db: Session, new_company:NewCompany):
    try:
        company_update = db.query(CompanyInfo).filter(CompanyInfo.company_id == new_company.company_id).first()
        if not company_update:
            return False  # 找不到公司
        if new_company.name is not None:
            company_update.name = new_company.name
        if new_company.url is not None:
            company_update.url = new_company.url
        if new_company.description is not None:
            company_update.description = new_company.description

        if new_company.name is not None or new_company.url is not None or new_company.description is not None:
            db.commit()
            response = True
            return True  # 更新成功
        else:
            return False  # 没有提供要更新的字段
    except Exception as e:
        print(e)
        db.rollback()  
        response = False
    return response  

#新增某一間公司的Tags
def update_company_tags(company_id: int, tag_ids: List[int], db: Session):
    try:
        # Find the company with the given company_id
        company = db.query(CompanyInfo).filter(CompanyInfo.company_id == company_id).first()

        if company:
            # Remove existing tag associations for this company
            db.query(ComTag).filter(ComTag.company_id == company_id).delete()

            # Add new tag associations
            for tag_id in tag_ids:
                db_add_companyID = ComTag(company_id=company_id, tag_id=tag_id)
                db.add(db_add_companyID)
            
            db.commit()
            response = {"message": "Tags updated successfully"}
        else:
            response = {"message": "Company not found"}

    except Exception as e:
        print(e)
        response = {"message": "An error occurred"}

    return response



#更新公司所有資訊跟TAGS
def update_company_and_tags(
    db: Session,
    new_company: AllNewCompany,
):
    try:
        # 查询要更新的公司
        company_update = db.query(CompanyInfo).filter(CompanyInfo.company_id == new_company.company_id).first()
        if not company_update:
            raise HTTPException(status_code=404, detail="Company not found")

        if new_company.name is not None:
            company_update.name = new_company.name
        if new_company.url is not None:
            company_update.url = new_company.url
        if new_company.description is not None:
            company_update.description = new_company.description

        db.query(ComTag).filter(ComTag.company_id == new_company.company_id).delete()

        tags_added = False

        for tag_id in new_company.tag_ids:
            tag_exists = db.query(ProductInfo).filter(ProductInfo.tag_id == tag_id).first()
            if tag_exists:
                db_add_companyID = ComTag(company_id=new_company.company_id, tag_id=tag_id)
                db.add(db_add_companyID)
                tags_added = True

        db.commit()

        if tags_added:
            response = {"message": "Company and tags updated successfully"}
        else:
            response = {"message": "Don't have the same tags in the database"}

    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="An error occurred while updating company and tags")

    return response

#比較表中所有符合條件的公司
def compare_table(compare_company: CompareCompany, db: Session):
    result = []

    for company_name in compare_company.company_name:
        id_detail = db.query(CompanyInfo.company_id).filter(CompanyInfo.name == company_name).first()
        tag_id_detail = db.query(ProductInfo.tag_id).filter(ProductInfo.tag_name == compare_company.tag_name).first() 
        function_id_detail = db.query(ComTag.function_id).filter(ComTag.tag_id == tag_id_detail & ComTag.company_id == id_detail).all()
        function_all = db.query(FunInfo).filter(FunInfo.function_id.in_(function_id_detail)).all()

        company_result = {
            "tag_name": compare_company.tag_name,
            "company_name": company_name,
            "Functions": [fun.function_name for fun in function_all],
        }
        result.append(company_result)

    return result
    # id_detail = db.query(CompanyInfo.company_id).filter(CompanyInfo.name == compare.company_name).first()
    # tag_id_detail = db.query(ProductInfo.tag_id).filter(ProductInfo.tag_name == compare.tag_name).first() 
    # function_id_detail = db.query(ComTag.function_id).filter(ComTag.tag_id == tag_id_detail & ComTag.company_id == id_detail ).all()
    # function_all = db.query(FunInfo).filter(FunInfo.function_id.in_(function_id_detail)).all()
    # # id_detail = [result.tag_id for result in id_detail]
    # # tag_company = db.query(FunInfo).filter(FunInfo.function_id.in_(function_id_detail)).all()
    # # company_detail = (
    # #     db.query(CompanyInfo).filter(CompanyInfo.company_id == company_id).all()
    # # )
    
    # sum = {
    #     "tag_name": compare.tag_name,
    #     "company_name": compare.company_name,
    #     "Functions" : [fun.function_name for fun in function_all],
    # }
    # return sum