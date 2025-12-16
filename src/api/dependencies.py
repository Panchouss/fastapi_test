from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_session
from src.schemas.books import PaginationParams, BookAddSchema


SessionDep = Annotated[AsyncSession,Depends(get_session)]
PoliyaDep = Annotated[BookAddSchema, Depends()]

PaginationDep = Annotated[PaginationParams,Depends(PaginationParams)]