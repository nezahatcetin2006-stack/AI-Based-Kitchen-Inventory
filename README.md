# Smart Pantry Pal

AI destekli mutfak envanter uygulaması.
Kullanıcılar ürünleri manuel veya fotoğrafla ekleyebilir, son kullanıma yaklaşan ürünleri takip edebilir ve envanteri kullanarak AI tarif önerileri alabilir.

## Özellikler

- Envanter ürünlerini listeleme
- Manuel ürün ekleme (sadece ürün adı, miktar, birim)
- Fotoğraftan ürün tanıma ve onayla ekleme
- Son kullanıma yaklaşan ürünleri görsel olarak vurgulama
- Ürün silme
- AI Şef: envanterde özellikle tarihi yakın ürünleri önceliklendirerek tarif önerme

## Canlı Demo
Yayın Linki:https://smart-pantry-pal-57.lovable.app
Canlı Demo:

## Teknoloji Yığını

- Frontend: Next.js (TypeScript, Tailwind CSS)
- Backend: FastAPI + SQLAlchemy
- Veritabanı: PostgreSQL
- AI: Groq (`llama-3.2-11b-vision-preview`)

## Nasıl Çalıştırılır?

### 1) Veritabanı (Opsiyonel Docker)

Proje kökünde:

```bash
docker compose up -d
```

### 2) Backend

`backend/.env` dosyası:

```env
PORT=8000
DATABASE_URL=postgresql+psycopg2://inventory:inventory@localhost:5432/kitchen_inventory
CORS_ORIGINS=http://localhost:3000,http://localhost:3001
SEED_DEMO=1
GROQ_API_KEY=YOUR_GROQ_API_KEY
GROQ_MODEL=llama-3.2-11b-vision-preview
VISION_MAX_IMAGE_BYTES=4194304
```

Backend'i çalıştır:

```bash
cd backend
py -m pip install -r requirements.txt
py -m uvicorn app.main:app --reload --port 8000
```

### 3) Frontend

`frontend/.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Frontend'i çalıştır:

```bash
cd frontend
npm install
npm run dev
```

## API Uç Noktaları

### Products
- `GET /products` - ürünleri listeler
- `POST /products` - manuel ürün ekler (kalan gün/saklama tavsiyesi AI ile tamamlanır)
- `DELETE /products/{id}` - ürün siler

### AI Entry
- `POST /products/ai-entry` - fotoğraftan ürün önizlemesi üretir

### AI Şef
- `POST /recipes/ai-chef` - envanteri kullanarak tarif önerisi üretir (tarihi yakın ürünleri önceliklendirir)

## Kısa Doğrulama

1. Envanter listesi açılıyor mu kontrol et.
2. Manuel ürün eklemede yalnızca 3 alan (ad, miktar, birim) görünüyor mu kontrol et.
3. Fotoğraftan ürün ekleme akışı çalışıyor mu kontrol et.
4. `Tarif Önerisi Al` butonu tarif döndürüyor mu kontrol et.
5. Ürün silme butonu çalışıyor mu kontrol et.

## Notlar

- `DELETE /products/{id}` için 404 alırsan backend'i yeniden başlat.
- Aynı anda birden fazla uvicorn süreci çalışırsa rota davranışı karışabilir; tek backend süreciyle devam et.
