import datetime as dt

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.product import Product as ProductModel
from app.schemas.product import Unit


def seed_demo_products(db: Session) -> None:
    existing_count = db.execute(select(func.count(ProductModel.id))).scalar_one()
    if existing_count > 0:
        return

    now = dt.datetime.now(dt.timezone.utc)
    demo_products = [
        ProductModel(
            name="Süt",
            quantity=1,
            unit=Unit.adet.value,
            estimatedExpirationDays=5,
            storageAdvice="Buzdolabı (4°C civarı)",
            createdAt=now - dt.timedelta(days=3),
            updatedAt=now - dt.timedelta(days=3),
        ),
        ProductModel(
            name="Yoğurt",
            quantity=1,
            unit=Unit.adet.value,
            estimatedExpirationDays=10,
            storageAdvice="Buzdolabı (2-6°C)",
            createdAt=now - dt.timedelta(days=8),
            updatedAt=now - dt.timedelta(days=8),
        ),
        ProductModel(
            name="Elma",
            quantity=3,
            unit=Unit.adet.value,
            estimatedExpirationDays=15,
            storageAdvice="Serin ve kuru yer",
            createdAt=now - dt.timedelta(days=14),
            updatedAt=now - dt.timedelta(days=14),
        ),
    ]

    db.add_all(demo_products)
    db.commit()

