# 🛠️ Teknoloji Yığını (Tech Stack)

Bu belge, **AI Destekli Mutfak Envanter Yönetimi** projesinde kullanılan tüm dilleri, kütüphaneleri ve araçları detaylandırır.

---

## 🎨 Frontend (Önyüz)
Kullanıcı arayüzü, hız ve modern kullanıcı deneyimi odaklı teknolojilerle geliştirilmiştir.

-   **Framework:** [Next.js 14+](https://nextjs.org/) (App Router mimarisi)
-   **Kütüphane:** [React.js](https://reactjs.org/)
-   **Styling:** [Tailwind CSS](https://tailwindcss.com/) (Responsive ve modern tasarım için)
-   **İkon Seti:** [Lucide React](https://lucide.dev/)
-   **State Management:** React Hooks (useState, useEffect)
-   **HTTP Client:** Fetch API

## ⚙️ Backend (Sunucu)
Sunucu tarafı, yüksek performanslı ve asenkron veri işleme yeteneği için Python tabanlıdır.

-   **Dil:** [Python 3.12+](https://www.python.org/)
-   **Framework:** [FastAPI](https://fastapi.tiangolo.com/) (Hızlı, modern ve asenkron API yapısı)
-   **ORM:** [SQLAlchemy](https://www.sqlalchemy.org/) (Veritabanı işlemleri için)
-   **Veri Doğrulama:** [Pydantic v2](https://docs.pydantic.dev/)
-   **Web Server:** [Uvicorn](https://www.uvicorn.org/)

## 🗄️ Veritabanı (Database)
Veri güvenliği ve ilişkisel veri yapısı için endüstri standardı bir veritabanı seçilmiştir.

-   **Database:** [PostgreSQL](https://www.postgresql.org/)
-   **Bağlantı Sürücüsü:** [psycopg2-binary](https://www.psycopg.org/)

## 🤖 Yapay Zeka (Artificial Intelligence)
Görsel tanıma ve otomatik envanter girişi süreçleri için en güncel modeller kullanılmaktadır.

-   **LLM Service:** [Groq Cloud API](https://groq.com/)
-   **Model:** Llama-3-Vision / Llama-3-70b (Hızlı görsel analiz ve JSON veri üretimi)
-   **Entegrasyon:** Base64 görsel kodlama ve AI prompt mühendisliği.

## 🐳 Altyapı ve Dağıtım (Infrastructure)
Projenin her ortamda (Windows, Linux, macOS) sorunsuz çalışması için konteyner yapısı kurulmuştur.

-   **Containerization:** [Docker](https://www.docker.com/) & [Docker Compose](https://docs.docker.com/compose/)
-   **Version Control:** Git & [GitHub](https://github.com/)
-   **IDE:** [Cursor AI](https://www.cursor.com/)

---

## 📁 Proje Klasör Yapısı (Özet)
```text
AI-BASED-KITCHEN-INVENTORY/
├── backend/            # FastAPI Sunucusu ve Database Modelleri
├── frontend/           # Next.js Uygulaması ve Arayüz Bileşenleri
├── docs/               # Proje Dokümantasyonu (PRD, Tasks)
├── docker-compose.yml  # Docker Yapılandırması
└── .gitignore          # Gereksiz dosyaların engellenmesi
