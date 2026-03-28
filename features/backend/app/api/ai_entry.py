from fastapi import APIRouter, UploadFile, File, HTTPException
import logging

# Loglama ayarı: Terminalde her şeyi görebilmek için
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ÖNEMLİ: Groq kullanıyorsan groq_ai'den import ettiğinden emin ol
try:
    from app.ai.groq_ai import analyze_product_image
    logger.info("✅ Groq AI modülü başarıyla yüklendi.")
except ImportError as e:
    logger.error(f"❌ Import Hatası: {e}")
    # Eğer groq_ai.py yoksa gemini'yi dene
    from app.ai.gemini import analyze_product_image

from app.schemas.ai_entry import AiEntryPreview

router = APIRouter()

@router.post("/ai-entry", response_model=AiEntryPreview)
async def create_ai_entry_preview(file: UploadFile = File(...)):
    logger.info(f"--- YENİ İSTEK GELDİ: {file.filename} ---")
    
    if not file.content_type.startswith("image/"):
        logger.warning(f"Geçersiz dosya tipi: {file.content_type}")
        raise HTTPException(status_code=400, detail="Lütfen bir resim dosyası yükleyin.")

    try:
        contents = await file.read()
        logger.info(f"Dosya okundu, boyut: {len(contents)} bytes. AI'ya gönderiliyor...")
        
        # Analiz fonksiyonunu çağır
        result = await analyze_product_image(image_bytes=contents, mime_type=file.content_type)
        
        logger.info("✅ AI Analizi başarıyla tamamlandı!")
        return result

    except Exception as e:
        logger.error(f"💥 AI ANALİZ SIRASINDA KRİTİK HATA: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=500, 
            detail=f"Sunucu tarafında hata oluştu: {str(e)}"
        )