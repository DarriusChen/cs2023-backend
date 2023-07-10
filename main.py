#主要後端的運作(連接)

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
#用來運行fastapi的伺服器
import uvicorn
#資料庫裡面的操作crud, model(格式)
from src import crud, model, function
#資料庫裡的table設定
from src.model import ProductInfo,  CompanyInfo, ComTag
#檢查輸入的資料格式是否正確
from src.schema import CompanyCreate, ProductCreate, ComTagFormat
#連接到資料庫的位置
from src.database import SessionLocal, engine
#有ORM後用Session跟DB的Engine的連接
from sqlalchemy.orm.session import Session

#CreateTime = Column(DateTime, nullable=False, default=datetime.now())

model.Base.metadata.create_all(bind=engine)


app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#當剛進入網頁時就傳送所有json資料
@app.post('/')
def read(db: Session = Depends(get_db)):
    return crud.read_all_data(db)

#建立產品TAG(OK)
@app.post('/createProduct/')
def create(product:ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)
#建立公司的Detail(OK)
@app.post('/createCompany/')
def create(company:CompanyCreate, db: Session = Depends(get_db)):
    if crud.create_company(db, company):
        return "Success"
    else:
         False

#給company_id獲得公司的Detail(OK)
@app.post('/getCompany/')
def get_company(company_id:int, db: Session = Depends(get_db)):
    return crud.get_company(db, company_id)

#給Product_id獲得公司的Detail(OK)
@app.post('/getProduct/')
def get_product(tag_id:int, db: Session = Depends(get_db)):
    return crud.get_product(db, tag_id)

#輸入company_id找他有的tag內容
@app.post('/getComTag/')
def get_company_tag(company_id:int, db: Session = Depends(get_db)):
    return crud.get_company_tag(db, company_id)

#, response_model=ComTagFormat

#輸入tag找他有的company內容
@app.post('/getTagCom/')
def get_company_tag(tag_id:int, db: Session = Depends(get_db)):
    return crud.get_tag_company(db, tag_id)

#更新資料庫資料
# @app.post('/UpdateCompany/')
# def Update()


if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
