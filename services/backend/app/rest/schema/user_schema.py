from pydantic import BaseModel

class UserSignUpDTO(BaseModel):
    username: str
    email: str
    password: str

class UserLoginDTO(BaseModel):
    email: str
    password: str

class UserResponseDTO(BaseModel):
    id: int
    username: str
    email: str