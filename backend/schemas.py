from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, Literal
from datetime import datetime

class TokenData(BaseModel):
    id: int


class UserRead(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")


class Token(BaseModel):
    access_token: str
    token_type: str


class FolderCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Folder name cannot be empty or exceed 255 characters")
    parent_id: Optional[int] = None

    @validator('name')
    def name_must_not_be_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Folder name cannot be empty or just whitespace')
        return v.strip()


class FolderRead(BaseModel):
    id: int
    name: str
    parent_id: Optional[int] = None

    class Config:
        from_attributes = True


class FolderRename(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)

    @validator('name')
    def name_must_not_be_whitespace(cls, v):
        if not v.strip():
            raise ValueError('Folder name cannot be empty or just whitespace')
        return v.strip()


class AccessCreate(BaseModel):
    access_type: Literal['only_me', 'anyone_with_link', 'timed_access']
    time_unit: Optional[Literal['minutes', 'hours', 'days']] = None
    time_value: Optional[int] = Field(None, gt=0, description="Time value must be positive")


class FileAccess(BaseModel):
    access_type: str
    share_token: Optional[str] = None
    expiry_time: Optional[datetime] = None

    class Config:
        from_attributes = True
