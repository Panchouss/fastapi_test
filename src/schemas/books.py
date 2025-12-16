from pydantic import BaseModel, Field


class BookAddSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookAddSchema):
    id: int

class PaginationParams(BaseModel):
    limit: int = Field(1, ge=0, le=100, description="Количество элементов на странице")
    offset: int = Field(0, ge=0, description="Смещение для пагинации")

