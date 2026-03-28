# Backend (FastAPI)

## Geliştirme
1. `backend/.env.example` dosyasını kopyalayın: `.env`
2. (Opsiyonel) DB için `docker-compose.yml` içindeki `postgres` servisini başlatın.
3. Backend’i çalıştırın:
   - `pip install -r requirements.txt`
   - `uvicorn app.main:app --reload --port 8000`

## API
- `GET /products`
- `POST /products`
- `POST /products/ai-entry` (fotoğraf -> Groq Vision önizleme)

## Groq Vision
`.env` içinde aşağıdakileri tanımlayın:
- `GROQ_API_KEY`
- `GROQ_MODEL` (varsayılan: `llama-3.2-11b-vision-preview`)
- `VISION_MAX_IMAGE_BYTES` (varsayılan: 4194304 ~ 4MB)

