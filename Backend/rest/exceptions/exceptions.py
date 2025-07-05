from fastapi import HTTPException

class UserNotFoundException(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="User not found")

class UserAlreadyExistsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=409, detail="User already exists")

class InvalidCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Wrong email or password")

class InvalidTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="Invalid Token")

class NotExistingTokenException(HTTPException):
    def __init__(self):
        super().__init__(status_code=401, detail="No token found")

class DataBaseFailException(HTTPException):
    def __init__(self):
        super().__init__(status_code=500, detail="DataBase fail")