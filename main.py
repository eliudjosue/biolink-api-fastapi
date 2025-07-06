from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
from routes.links import router
from routes.auth import auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router)
app.include_router(auth_router)
