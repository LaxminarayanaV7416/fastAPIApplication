from pydantic import BaseModel
from typing import Optional, List

class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str

class RegisterRequestSchema(BaseModel):
    email: str
    password: str

class CurrentUserSchema(BaseModel):
    email: str