import uvicorn
from fastapi import FastAPI
from src.api import main_router
from fastapi.middleware.cors import CORSMiddleware
from src.middlewr.logic import http_performance_middleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:63342"], # или * чтобы любые другие сайты могли подключатся к нашему api
)

app.middleware("http")(http_performance_middleware)

app.include_router(main_router)






#
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", reload=True)
