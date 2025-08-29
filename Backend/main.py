from fastapi import FastAPI
from contextlib import asynccontextmanager
from rest.model.database import Base, async_engine, close_db_connection
from rest.exceptions.global_exception_handler import add_exception_handlers
from rest.controller.user_account_controller import user_router
from rest.controller.token_controller import token_router
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
      "http://localhost:3000",
      "http://172.18.0.4:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add health check endpoint for Docker health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}