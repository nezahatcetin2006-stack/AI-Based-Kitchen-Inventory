import datetime as dt
from collections.abc import Generator

from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.ai.groq_ai import generate_recipe_suggestions_from_inventory
from app.db import SessionLocal
from app.models.product import Product as ProductModel
from app.schemas.recipe import RecipeSuggestionResponse


router = APIRouter()


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def compute_days_remaining(created_at: dt.datetime, estimated_expiration_days: int) -> int:
    now_date = dt.datetime.now(dt.timezone.utc).date()
    created_date = created_at.astimezone(dt.timezone.utc).date() if created_at.tzinfo else created_at.date()
    days_elapsed = (now_date - created_date).days
    return max(0, estimated_expiration_days - days_elapsed)


@router.post("/ai-chef", response_model=RecipeSuggestionResponse, status_code=status.HTTP_200_OK)
async def ai_chef_recipe_suggestions(db: Session = Depends(get_db)) -> RecipeSuggestionResponse:
    products = db.execute(select(ProductModel).order_by(ProductModel.createdAt.desc())).scalars().all()

    inventory_rows = [
        {
            "name": p.name,
            "quantity": p.quantity,
            "unit": p.unit,
            "daysRemaining": compute_days_remaining(p.createdAt, p.estimatedExpirationDays),
            "storageAdvice": p.storageAdvice,
        }
        for p in products
    ]
    inventory_rows.sort(key=lambda x: x["daysRemaining"])

    return await generate_recipe_suggestions_from_inventory(inventory_rows=inventory_rows)

