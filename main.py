from datetime import timedelta
from typing import Annotated
import time
import asyncio

import uvicorn
from fastapi import FastAPI, HTTPException, Response, Depends, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field
from pyexpat.errors import messages
from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from authx import AuthX, AuthXConfig
from starlette.responses import StreamingResponse

app = FastAPI()

config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)

class UserLogitSchema(BaseModel):
    username: str
    password: str

@app.post("/login",tags=["Пользователь👨🏻‍"])
def login(creads: UserLogitSchema, response: Response):
    if creads.username == "test" and creads.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.get("/protected",
         tags=["Пользователь👨🏻‍"],
         dependencies=[Depends(security.access_token_required)]
         )
def get_protected():
    return {"message": "Hello World"}

async def async_task():
    await asyncio.sleep(3)
    print("Пользователь получен")

engine = create_async_engine('sqlite+aiosqlite:///books.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession,Depends(get_session)]

class Base(DeclarativeBase):
    pass

class BooksModel(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author: Mapped[str]

@app.post("/create_database",tags=["Книги📚"])
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True }

class BookAddSchema(BaseModel):
    title: str
    author: str

class BookSchema(BookAddSchema):
    id: int


@app.post("/books",tags=["Книги📚"])
async def add_book(data: BookAddSchema, session: SessionDep):
    new_book = BooksModel(
        title=data.title,
        author=data.author
    )
    session.add(new_book)
    await session.commit()
    return {"ok добавленно": True}

def inerfile(filename: str):
    with open(filename, "rb") as file:
        while chunk := file.read(1024*1024):
            yield chunk

@app.get("/files/streaming/{filename}",tags=["Книги📚"])
async def get_streaming_files(filename: str):
    return StreamingResponse(inerfile(filename), media_type="video/mp4")

@app.post("/uploaded",tags=["Книги📚"])
async def uploaded_file(uploaded_photo: UploadFile):
    file = uploaded_photo.file
    filename = uploaded_photo.filename
    with open(filename, "wb") as f:
        f.write(file.read())



@app.get("/books/{book_id}",tags=["Книги📚"],summary="Получить конкретную книгу")
async def get_book(book_id: int, session: SessionDep):
    query = select(BooksModel).filter(BooksModel.id == book_id)
    result = await session.execute(query)
    book = result.scalar_one_or_none()
    asyncio.create_task(async_task()) #выполнить на фоне определенную функцию
    if book is None:
        raise HTTPException(status_code=404, detail=f"Книга с id {book_id} не найдена")
    return book
    # return result.scalars().all()

# books = [
#     {
#         "id": 1,
#         "title": "3k elo solo",
#         "author": "panchous",
#     },
#     {
#         "id": 2,
#         "title": "2k elo uznik",
#         "author": "kizze",
#     },
# ]


# @app.get("/books",
#          tags=["Книги📚"],
#          summary="Получить все книги"
#          )
# def read_books():
#     return books
#
# @app.get("/books/{books_id}",
#          tags=["Книги📚"],
#          summary="Получить конкретную книгу"
#         )
# def read_book(book_id: int):
#     for book in books:
#         if book["id"] == book_id:
#             return book
#     raise HTTPException(status_code=404, detail="Book not found")
#
# class New_Book(BaseModel):
#     title: str
#     author: str = Field()
#
# @app.post("/books",tags=["Книги📚"])
# def create_book(new_book: New_Book):
#     books.append({
#         "id": len(books) + 1,
#         "title": new_book.title,
#         "author": new_book.author,
#     })
#     return {"success": True, "message": "Книга успешно добавлена"}




if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", reload=True )