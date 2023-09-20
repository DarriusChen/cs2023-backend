# 當新增或是建立數據的時候會有設定好的資料類型

from typing import List

# 用typing記住屬性類別，並且用BaseModel進行資料驗證
from pydantic import BaseModel


# 輸入的公司名稱
class CompanyBase(BaseModel):
    #company_id: int
    name: str
    url: str | None = None
    description: str | None = None
    tag_id: List[int] = [] 


class CompanyCreate(CompanyBase):
    pass


# 輸入的商品名稱
class ProductBase(BaseModel):
    tag_name: str
    tag_category: str


class ProductCreate(ProductBase):
    pass




class NewCompany(BaseModel):
    company_id: int
    name: str | None = None
    url: str | None = None
    description: str | None = None
    

class AllNewCompany(BaseModel):
    company_id: int
    name: str | None = None
    url: str | None = None
    description: str | None = None
    tag_ids: List[int] | None = None

class CompareCompany(BaseModel):
    company_name: List[str] | None = None
    tag_name: str | None = None
