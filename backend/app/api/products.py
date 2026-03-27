import datetime as dt
from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import SessionLocal
from app.ai.groq_ai import analyze_product_text
from app.models.product import Product as ProductModel
from app.schemas.product import ProductCreate, ProductOut


router = APIRouter() # tags kısmını main.py'da yöneteceğiz, burayı temiz tutalım.


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def compute_days_remaining(created_at: dt.datetime, estimated_expiration_days: int) -> int:
    # UTC üzerinden gün hesabı yapıyoruz ki farklı saat dilimlerinde tutarlılık korunsun.
    now_date = dt.datetime.now(dt.timezone.utc).date()
    created_date = created_at.astimezone(dt.timezone.utc).date() if created_at.tzinfo else created_at.date()
    days_elapsed = (now_date - created_date).days
    remaining = estimated_expiration_days - days_elapsed
    return max(0, remaining)


# DÜZELTME: Rota "/products" yerine "/" oldu. 
# Çünkü main.py'da zaten prefix="/products" ekledik.
@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate, db: Session = Depends(get_db)) -> ProductOut:
    try:
        estimated_days = payload.estimatedExpirationDays
        storage_advice = payload.storageAdvice

        # Manuel ekleme: UI sadece name/quantity/unit gönderir.
        # Eksikse, Groq'tan metin üzerinden tahmin alıp dolduruyoruz.
        if estimated_days is None or storage_advice is None:
            preview = await analyze_product_text(
                product_name=payload.name,
                quantity=payload.quantity,
                unit=payload.unit.value,
            )
            estimated_days = preview.estimatedStorageDays
            storage_advice = preview.storageAdvice

        product = ProductModel(
            name=payload.name,
            quantity=payload.quantity,
            unit=payload.unit.value,
            estimatedExpirationDays=estimated_days,
            storageAdvice=storage_advice,
        )
        db.add(product)
        db.commit()
        db.refresh(product)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Ürün kaydedilemedi: {e}") from e

    days_remaining = compute_days_remaining(product.createdAt, product.estimatedExpirationDays)
    return ProductOut(
        id=product.id,
        name=product.name,
        quantity=product.quantity,
        unit=product.unit,
        estimatedExpirationDays=product.estimatedExpirationDays,
        storageAdvice=product.storageAdvice,
        createdAt=product.createdAt,
        daysRemaining=days_remaining,
    )


# DÜZELTME: Rota "/products" yerine "/" oldu.
@router.get("/", response_model=list[ProductOut])
def list_products(db: Session = Depends(get_db)) -> list[ProductOut]:
    products = db.execute(select(ProductModel).order_by(ProductModel.createdAt.desc())).scalars().all()

    out: list[ProductOut] = []
    for product in products:
        out.append(
            ProductOut(
                id=product.id,
                name=product.name,
                quantity=product.quantity,
                unit=product.unit,
                estimatedExpirationDays=product.estimatedExpirationDays,
                storageAdvice=product.storageAdvice,
                createdAt=product.createdAt,
                daysRemaining=compute_days_remaining(product.createdAt, product.estimatedExpirationDays),
            )
        )
    return out


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db)) -> None:
    product = db.get(ProductModel, id)
    if not product:
        raise HTTPException(status_code=404, detail="Ürün bulunamadı.")

    db.delete(product)
    db.commit()