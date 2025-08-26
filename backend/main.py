from fastapi import FastAPI
from backend.routers import chat, structured, health

app = FastAPI()

app.include_router(chat.router)
app.include_router(structured.router)
app.include_router(health.router)
