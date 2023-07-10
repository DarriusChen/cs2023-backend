#資料前處理

import json
from sqlalchemy.orm import Session, session
from src.model import ProductInfo, CompanyInfo

#開始進入資料庫將所有的資料轉成json檔給前端
def Convert_JSON(db):
    
    # 執行 SQL 查詢
    data = db.query("SELECT * FROM Company_Detail left join Product_Detail on Company_Detail.tag_id=Product_Detail.tag_id")
    json_data = json.dumps(data)
    return json_data

