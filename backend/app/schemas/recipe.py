from pydantic import BaseModel, Field


class RecipeSuggestion(BaseModel):
    recipeTitle: str = Field(min_length=1, max_length=200)
    ingredients: list[str] = Field(default_factory=list)
    steps: list[str] = Field(default_factory=list)
    servings: int | None = Field(default=None, ge=1, le=20)
    calories: int | None = Field(default=None, ge=0, le=5000)
    focusProducts: list[str] = Field(default_factory=list, description="Özellikle değerlendirilen ürünler")
    note: str = Field(default="", max_length=500)


class RecipeSuggestionResponse(BaseModel):
    recipes: list[RecipeSuggestion] = Field(default_factory=list)

