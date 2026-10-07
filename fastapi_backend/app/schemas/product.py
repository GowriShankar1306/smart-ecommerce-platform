from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=200)
    description: str | None = None
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    category_id: int = Field(gt=0)
    image: str | None = None


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str | None = None
    price: float
    stock: int
    category_id: int
    image: str | None = None

    class Config:
        from_attributes = True