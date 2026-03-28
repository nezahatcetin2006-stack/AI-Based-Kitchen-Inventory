import datetime as dt
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Unit(str, Enum):
    adet = "adet"
    gram = "gram"
    kilo = "kilo"


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    quantity: float = Field(ge=0, le=100000)
    unit: Unit
    # Manuel ekleme akışında kullanıcı bu alanları girmeyecek.
    # Eğer eksik gelirse backend otomatik doldurur.
    estimatedExpirationDays: int | None = Field(default=None, ge=0, le=3650)
    storageAdvice: str | None = Field(default=None, max_length=500)


class ProductOut(BaseModel):
    id: int
    name: str
    quantity: float
    unit: Unit
    estimatedExpirationDays: int
    storageAdvice: str
    createdAt: dt.datetime
    daysRemaining: int

    model_config = ConfigDict(from_attributes=True)

