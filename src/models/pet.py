from typing import Optional
from pydantic import BaseModel


class Category(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Tag(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None


class Pet(BaseModel):
    id: Optional[int] = None
    category: Optional[Category] = None
    name: Optional[str] = None          # required per spec; optional to tolerate demo API pollution
    photoUrls: Optional[list[str]] = None
    tags: Optional[list[Tag]] = None
    status: Optional[str] = None


class ApiResponse(BaseModel):
    code: Optional[int] = None
    type: Optional[str] = None
    message: Optional[str] = None
