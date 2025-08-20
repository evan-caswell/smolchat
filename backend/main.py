from fastapi import FastAPI
from routers import chat_router

app = FastAPI()

app.include_router(chat_router.router)
