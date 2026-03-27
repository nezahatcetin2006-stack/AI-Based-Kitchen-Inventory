# 🗺️ Kullanıcı Akış Şeması (User Flow)

Bu belge, **AI Destekli Mutfak Envanter Yönetimi** uygulamasını kullanan bir kullanıcının sistem içindeki yolculuğunu ve teknik etkileşim adımlarını açıklar.

---

## 1. Ana Sayfaya Giriş ve Veri Yükleme
* **Kullanıcı Eylemi:** Tarayıcı üzerinden `http://localhost:3000` adresine gider.
* **Sistem Yanıtı:** * **Frontend (Next.js):** Backend API'ye (`GET /api/products`) bir istek gönderir.
    * **Backend (FastAPI):** PostgreSQL veritabanındaki tüm ürünleri sorgular.
    * **Arayüz:** Mevcut envanter kartlar halinde kullanıcıya sunulur.

## 2. Manuel Ürün Ekleme Süreci
* **Kullanıcı Eylemi:** "Yeni Ürün Ekle" formuna ürün adını, miktarını ve birimini (kg, adet, l) girer.
* **Sistem Yanıtı:**
    * **Eylem:** "Ekle" butonuna basılır.
    * **Teknik Akış:** Veriler JSON formatında `/api/products` endpoint'ine `POST` edilir.
    * **Sonuç:** Veritabanına yeni satır eklenir ve liste anlık (UI re-render) güncellenir.

## 3. AI Destekli (Görselden) Ürün Tanımlama
* **Kullanıcı Eylemi:** Mutfaktaki bir ürünün (örneğin bir elma veya süt kutusu) fotoğrafını yükler.
* **Sistem Yanıtı:**
    * **İşlem:** Görsel `multipart/form-data` olarak Backend'e iletilir.
    * **AI Entegrasyonu:** FastAPI, görseli **Groq AI (Llama-3-Vision)** modeline gönderir.
    * **Analiz:** Yapay zeka görseldeki nesneyi ve miktarını tespit eder.
    * **Onay:** AI'dan gelen veriler (Ürün: Süt, Miktar: 1) form alanlarına otomatik dolar. Kullanıcı onayladığında envantere eklenir.

## 4. Envanter Yönetimi (Güncelleme & Silme)
* **Stok Güncelleme:**
    * Kullanıcı kart üzerindeki `+` veya `-` butonlarına tıklar.
    * Sistem, `/api/products/{id}` adresine `PATCH` isteği göndererek miktarı veritabanında günceller.
* **Ürün Silme:**
    * Kullanıcı "Sil" ikonuna tıklar.
    * Sistem, ilgili ürünü `DELETE` isteği ile veritabanından kalıcı olarak kaldırır.

## 5. Kritik Stok Uyarı Sistemi
* **Algoritma:** Her ürünün mevcut miktarı, sistem tarafından belirlenen "kritik eşik" ile karşılaştırılır.
* **Görsel Geri Bildirim:**
    * Miktar > 5 ise: **Yeşil** (Yeterli stok).
    * Miktar <= 5 ise: **Sarı** (Azalıyor).
    * Miktar <= 2 ise: **Kırmızı** (Kritik - Alışveriş listesine eklenmeli).

---

## Teknik Özet
| Adım | Yöntem | Endpoint | Açıklama |
| :--- | :--- | :--- | :--- |
| **Listeleme** | GET | `/api/products` | Mevcut envanteri getirir. |
| **Ekleme** | POST | `/api/products` | Yeni ürünü kaydeder. |
| **AI Analiz** | POST | `/api/ai/analyze` | Görseli AI ile işler. |
| **Güncelleme** | PATCH | `/api/products/{id}` | Stok miktarını değiştirir. |
| **Silme** | DELETE | `/api/products/{id}` | Ürünü sistemden kaldırır. |
