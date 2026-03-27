# Stack Kararları

## Neden Next.js + FastAPI?
- Frontend’de hızlı UI geliştirme ve iyi geliştirici deneyimi için React/Next.js.
- Backend’de temiz API tasarımı, validation ve hızlı iterasyon için FastAPI.

## Seçilen paketler / yaklaşım
- Frontend: Next.js App Router, TypeScript, Tailwind CSS.
- Backend: FastAPI + SQLAlchemy + PostgreSQL.
- Basit MVP için API:
  - `GET /products`: Ürünleri listele (kalan gün bilgisi hesaplanmış döner)
  - `POST /products`: Manuel ürün ekle

## Çevresel değişkenler
- Frontend: `NEXT_PUBLIC_API_BASE_URL`
- Backend: `DATABASE_URL`, `CORS_ORIGINS`, `SEED_DEMO`

