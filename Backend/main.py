from fastapi import FastAPI
from contextlib import asynccontextmanager
from rest.model.database import Base, async_engine, close_db_connection
from rest.exceptions.global_exception_handler import add_exception_handlers
from rest.controller.user_account_controller import user_router
from rest.controller.token_controller import token_router

# database connection
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await close_db_connection()

app = FastAPI(lifespan=lifespan)

add_exception_handlers(app)

app.include_router(user_router)
app.include_router(token_router)