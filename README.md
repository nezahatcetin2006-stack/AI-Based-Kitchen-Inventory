# AI Based Kitchen Inventory - READ

Bu proje, mutfak envanterini takip etmenizi ve ürünleri iki farklı şekilde eklemenizi sağlar:
- Manuel ekleme: kullanıcı `ürün adı + miktar + birim` girer, kalan gün/saklama tavsiyesi AI ile otomatik tamamlanır.
- Fotoğraftan ekleme: görsel analiz ile ürün bilgileri önerilir ve onayla listeye eklenir.

## Teknoloji
- Frontend: Next.js (TypeScript, Tailwind)
- Backend: FastAPI + SQLAlchemy
- Veritabanı: PostgreSQL
- AI: Groq Vision (`llama-3.2-11b-vision-preview`)

## Proje yapısı
- `frontend/` - kullanıcı arayüzü
- `backend/` - API ve AI iş mantığı
- `docs/` - ek dokümantasyon

## Gereksinimler
- Node.js 18+
- Python 3.10+
- PostgreSQL (veya Docker)

## Kurulum

### 1) Veritabanı (opsiyonel Docker ile)
Kök dizinde:

```bash
docker compose up -d
```

### 2) Backend
`backend/.env` dosyasını aşağıdaki örneğe göre doldurun:

```env
PORT=8000
DATABASE_URL=postgresql+psycopg2://inventory:inventory@localhost:5432/kitchen_inventory
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
SEED_DEMO=1
GROQ_API_KEY=YOUR_GROQ_KEY
GROQ_MODEL=llama-3.2-11b-vision-preview
VISION_MAX_IMAGE_BYTES=4194304
```

Ardından:

```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload --port 8000
```

### 3) Frontend
`frontend/.env.local` dosyasını oluşturun:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Ardından:

```bash
cd frontend
npm install
npm run dev
```

## API uç noktaları
- `GET /products` - ürünleri listeler
- `POST /products` - manuel ürün ekler
- `DELETE /products/{id}` - ürün siler
- `POST /products/ai-entry` - fotoğraftan AI önizleme üretir

## Kısa test
1. Frontend açıldığında ürün listesi görünmeli.
2. Manuel ürün eklemede sadece 3 alan görünmeli: ad, miktar, birim.
3. Ürün eklendikten sonra kalan gün ve saklama tavsiyesi AI ile dolu gelmeli.
4. Bir ürünün `Sil` butonu çalışmalı.

## Notlar
- Eğer `DELETE /products/{id}` 404 alırsanız backend'i yeniden başlatın.
- Birden fazla `uvicorn` süreci çalışıyorsa port çakışması/yanlış rota davranışı olabilir.
