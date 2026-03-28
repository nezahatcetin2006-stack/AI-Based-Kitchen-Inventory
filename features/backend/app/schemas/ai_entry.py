from enum import Enum

from pydantic import BaseModel, Field


class AiEntryUnit(str, Enum):
    # Product birimlerini aynı değerlerle koruyoruz.
    adet = "adet"
    gram = "gram"
    kilo = "kilo"


class AiEntryPreview(BaseModel):
    productName: str = Field(min_length=1, max_length=255)
    quantityEstimate: float = Field(ge=0, le=100000)
    unit: AiEntryUnit = Field(description="Unit: adet | gram | kilo")
    estimatedStorageDays: int = Field(ge=0, le=3650)
    storageAdvice: str = Field(min_length=1, max_length=500)
    confidence: float = Field(ge=0, le=1, description="0-1 arası güven skoru")

