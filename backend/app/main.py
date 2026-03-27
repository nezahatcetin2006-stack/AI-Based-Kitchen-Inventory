from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.products import router as products_router
from app.api.ai_entry import router as ai_entry_router
from app.config import settings
from app.db import Base, engine, SessionLocal
from app.seed import seed_demo_products

def create_app() -> FastAPI:
    application = FastAPI(title="AI Based Kitchen Inventory", version="1.0")

    # CORS Ayarları: Frontend (localhost:3000) ile Backend (localhost:8000) arasındaki engeli kaldırır
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], 
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # ÖNEMLİ DÜZELTME: 
    # Frontend terminalinde gördüğümüz "POST /products/ai-entry" adresini yakalamak için 
    # her iki router'ı da "/products" prefix'i altına topluyoruz.
    
    # 1. Ürün listeleme/ekleme rotaları (/products, /products/{id} vb.)
    application.include_router(products_router, prefix="/products", tags=["Products"])
    
    # 2. AI Analiz rotası (/products/ai-entry)
    # ai_entry_router içinde @router.post("/ai-entry") olduğu için başına /products ekliyoruz.
    application.include_router(ai_entry_router, prefix="/products", tags=["AI"])

    @application.on_event("startup")
    def on_startup() -> None:
        # Veritabanı tablolarını oluşturur
        Base.metadata.create_all(bind=engine)
        
        # Eğer .env dosyasında SEED_DEMO=1 ise örnek verileri yükler
        if settings.SEED_DEMO:
            db = SessionLocal()
            try:
                seed_demo_products(db)
            finally:
                db.close()

    return application

app = create_app()