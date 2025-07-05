from urllib.request import Request
from fastapi import FastAPI
from starlette.responses import JSONResponse
from Backend.rest.exceptions.exceptions import (UserNotFoundException,
                                                UserAlreadyExistsException,
                                                InvalidCredentialsException,
                                                InvalidTokenException,
                                                NotExistingTokenException,
                                                DataBaseFailException)


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(UserNotFoundException)
    async def user_not_found_handler(request: Request, exc: UserNotFoundException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(UserAlreadyExistsException)
    async def user_already_exists_handler(request: Request, exc: UserAlreadyExistsException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(InvalidCredentialsException)
    async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(InvalidTokenException)
    async def invalid_token_handler(request: Request, exc: InvalidTokenException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(NotExistingTokenException)
    async def not_existing_token_handler(request: Request, exc: NotExistingTokenException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})

    @app.exception_handler(DataBaseFailException)
    async def data_base_fail_handler(request: Request, exc: DataBaseFailException):
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.detail})
