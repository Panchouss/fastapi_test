from urllib.request import Request

from fastapi import APIRouter, UploadFile, HTTPException, middleware, FastAPI
import asyncio

from sqlalchemy import select
from starlette.responses import StreamingResponse

from src.api.dependencies import SessionDep, PaginationDep, PoliyaDep
from src.database import engine, Base
from src.models.books import BooksModel
from src.schemas.books import BookAddSchema, BookSchema

router = APIRouter()


async def async_task(): #функция для выполнения на фоне
    await asyncio.sleep(3)
    print("Книга получена")




# @router.post("/create_database",tags=["Книги📚"])
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     return {"ok": True }



@router.post("/books",tags=["Книги📚"])
async def add_book(data: PoliyaDep,  session: SessionDep):
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

@router.get("/files/streaming/{filename}",tags=["Книги📚"])
async def get_streaming_files(filename: str):
    return StreamingResponse(inerfile(filename), media_type="video/mp4")

@router.post("/uploaded",tags=["Книги📚"])
async def uploaded_file(uploaded_photo: UploadFile):
    file = uploaded_photo.file
    filename = uploaded_photo.filename
    with open(filename, "wb") as f:
        f.write(file.read())

@router.get("/books/all",tags=["Книги📚"],summary="Получить список книг")
async def get_all_books(session: SessionDep):
    query = select(BooksModel)
    result = await session.execute(query)
    book = result.scalars().all()
    asyncio.create_task(async_task())  # выполнить на фоне определенную функцию
    return book


@router.get("/books",tags=["Книги📚"],summary="Получить одну или несколько книг")
async def get_book(
        session: SessionDep,
        pagination: PaginationDep,
) -> list[BookSchema]:
    query = select(BooksModel).limit(pagination.limit).offset(pagination.offset)
    result = await session.execute(query)
    book = result.scalars().all()
    # if book is None:
    #     raise HTTPException(status_code=404, detail=f"Книга не найдена")
    asyncio.create_task(async_task())  # выполнить на фоне определенную функцию
    return book






