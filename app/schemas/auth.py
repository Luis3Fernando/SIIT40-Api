from pydantic import BaseModel, EmailStr

class LoginDTO(BaseModel):
    email: EmailStr
    password: str

class TokenRefreshRequestDTO(BaseModel):
    refreshToken: str

class LoginResponseDataDTO(BaseModel):
    id: int
    fullName: str
    email: str
    accessToken: str
    refreshToken: str
    tokenType: str