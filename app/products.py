from pydantic import BaseModel

class ProductCreate(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

    class Config:
        orm_mode = True