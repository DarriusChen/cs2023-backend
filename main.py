# 主要後端的運作(連接)
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# 用來運行fastapi的伺服器
import uvicorn, json

# 資料庫裡面的操作crud, model(格式)
from src import crud, model

# 資料庫裡的table設定
from src.model import ProductInfo, CompanyInfo, ComTag

# 檢查輸入的資料格式是否正確
from src.schema import CompanyCreate, ProductCreate, NewCompany, AllNewCompany

# 連接到資料庫的位置`05
# `
# from src.database import SessionLocal, engine

# 有ORM後用Session跟DB的Engine的連接
from sqlalchemy.orm.session import Session

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2


conn = psycopg2.connect(
    dbname='postgres',
    user='admin',
    host='0.0.0.0',
    password='admin'
)


engine = create_engine('postgresql+psycopg2://', creator=lambda: conn)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)




model.Base.metadata.create_all(bind=engine)


app = FastAPI(title="CS2023", description="2023資安大會競品分析API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

######先把資料匯入postgresql裡######
# db = SessionLocal()
# 讀取JSON檔案中的數據
def initialize_data(db: Session):
    with open('src/company_data.json', 'r') as json_file:
        json_data = json.load(json_file)

# 將JSON數據插入到Company_Detail表
    for data in json_data:
        company_info = CompanyInfo(**data)
        db.add(company_info)

# 提交更改並關閉Session
    db.commit()
    db.close()

######先把資料匯入postgresql裡######



# 當剛進入網頁時就傳送所有json資料
@app.get("/", description="當剛進入網頁時就傳送所有json資料")
def read_company(
    db: Session = Depends(get_db),
):
    return crud.read_company(db)


# 建立產品TAG(OK)
@app.post("/createProduct/", description="建立新的產品標籤跟種類")
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    if crud.create_product(db, product):
        return "Success"
    else:
        return False


# 建立公司的Detail(OK)
@app.post("/createCompany/", description="建立新的公司跟相關資訊")
def create(company: CompanyCreate, db: Session = Depends(get_db)):
    if crud.create_company(db, company):
        return "Success"
    else:
        return False


# 給company_id獲得公司的Detail(OK)
@app.get("/getCompany/", description="用company_id找一間公司的所有資訊包含Tag")
def get_company(cid: int, db: Session = Depends(get_db)):
    if crud.get_company(db, cid):
        return crud.get_company(db, cid)
    else:
        return False


# 給Product_id獲得公司的Detail(OK)
@app.get("/getProduct/")
def get_product(tag_id: int, db: Session = Depends(get_db)):
    if crud.get_product(db, tag_id):
        return crud.get_product(db, tag_id)
    else:
        return False



# # 輸入company_id找他有的tag內容
# @app.get("/getComTag/", description="輸入company_id找他有的tag內容")
# def get_company_tag(company_id: int, db: Session = Depends(get_db)):
#     if crud.get_company_tag(db, company_id):
#         return crud.get_company_tag(db, company_id)
#     else:
#         return False


# 讀取所有的function公司
@app.get("/CompanyFunction/", description="讀取所有公司對應的Tag及tag有的function")
def company_function(company_id:int, db: Session = Depends(get_db)):
    if crud.company_function(db, company_id):
        return crud.company_function(db, company_id)
    else:
        return False


#輸顯示所有Category裡所有的Tag_name
@app.get("/CategoryTag/", description="顯示所有Category裡所有的Tag_name")
def catergory_tag(db: Session = Depends(get_db)):
    return crud.category_tag(db)

# 刪除company_id對應的公司資料
@app.delete("/DeleteCompany/", description="輸入一間公司的id刪除公司的相關資訊")
def delete_company(company_id:int, db:Session = Depends(get_db)):
    if crud.delete_company(db, company_id):
        return "Success"
    else:
        return False

# 更新Company資料
@app.post("/UpdateCompany/", description="輸入一間公司的id跟要更新的內容，如果沒有要更新就留著空白")
def update_company(new_company:NewCompany, db:Session = Depends(get_db)):
    if crud.update_company(db, new_company):
        return "Success"
    else:
        return False
#更新公司的標籤，直接輸入多個tag的id在list中
@app.put("/updateCompanyTags/{company_id}", description="更新公司的標籤，直接輸入多個tag的id在list中")
def update_company_tags(company_id: int, tag_ids: list[int], db: Session = Depends(get_db)):
    if crud.update_company_tags(company_id, tag_ids, db):
        return "Success"
    else:
        return False

#更新公司所有的資訊(包含Tags)
@app.post("/updateAll/", description="更新公司的標籤，直接輸入多個tag的id在list中")
def update_company_and_tags(new_company:AllNewCompany, db: Session = Depends(get_db)):
    if crud.update_company_and_tags(db, new_company):
        return crud.update_company_and_tags(db, new_company)
    else:
        return False

#更新公司的標籤，直接輸入多個tag的id在list中，直接新增
@app.put("/AddCompanyTags/{company_id}", description="更新公司的標籤，直接輸入多個tag的id在list中")
def add_company_tags(company_id: int, tag_ids: list[int], db: Session = Depends(get_db)):
    if crud.add_company_tags(company_id, tag_ids, db):
        return "Success"
    else:
        return False

if __name__ == "__main__":
    db = SessionLocal()
    initialize_data(db)
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
