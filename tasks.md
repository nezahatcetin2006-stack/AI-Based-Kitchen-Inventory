# Tasks.md - AI Based Kitchen Inventory (Step-by-step)

Bu doküman `prd.md` içindeki MVP hedeflerine ve Faz 1-3 roadmap’ine göre uygulamayı parça parça geliştirmek için görev listesidir.

## Faz 1: Temel envanter listeleme ve manuel ekleme (MVP)

1. Proje iskeletini kur (frontend + backend klasörleri, temel yapı).
2. Stack seçimini netleştir (ör. Next.js + FastAPI veya React + Flask) ve kararları dokümante et.
3. Veritabanını seç ve yerel geliştirme için konfigure et (Firebase veya PostgreSQL).
4. Ürün modeli (schema) tanımla:
   - `name`, `quantity`, `unit` (adet/kilo/gram vb.)
   - `estimatedExpirationDays` veya “son tüketim tarihi” yaklaşımı
   - `storageAdvice` (buzdolabı/karanlık yer vb.)
   - `createdAt`, `updatedAt`
5. Backend için temel API’leri tasarla ve uygula:
   - `POST /products` (manuel ürün ekleme)
   - `GET /products` (listeleme)
   - (opsiyonel) `DELETE /products/:id`
6. Frontend envanter ekranını oluştur:
   - Ürünleri listele (isim, miktar, kalan gün sayısı)
   - Basit ürün ekleme formu (manuel giriş)
7. Kalan gün sayısı hesaplama mantığını (veya backend’den gelen alanları) UI’da doğru göster.
8. “Kritik uyarı” görsel mantığını uygula:
   - Son 2 gün kalan ürünleri kırmızı/turuncu tonlarla vurgula
9. Temel doğrulama ekle:
   - Eksik alanlar için kullanıcı uyarıları
   - Miktar için basit sayı aralığı kontrolleri
10. Basit seed/test verisi ekle (geliştirme sırasında görmek için).
11. Uçtan uca “manuel ekle -> listeye düşme” akışını test et.

## Faz 2: AI ile fotoğraftan ürün tanıma entegrasyonu

1. Fotoğraf yükleme akışını tasarla:
   - Dosya seçme / drag-drop
   - Boyut/format limitleri
2. Backend’de dosya kabul etme endpoint’i ekle:
   - `POST /products/ai-entry` (fotoğraf -> AI süreç)
3. AI çağrısı için entegrasyon noktası oluştur:
   - Groq Vision entegrasyonunu belirle
4. Prompt/çıktı şemasını sabitle:
   - Çıktıda `productName`, `quantityEstimate`, `estimatedStorageDays` (veya türetilen alanlar)
   - Beklenen JSON formatını garanti altına al
5. AI sonuçlarını kullanıcıya “önizleme” olarak döndür:
   - Ürün ad/ miktar tahminini ve kalan gün bilgisi önerisini göster
6. “Manuel Onay” ekranını uygula:
   - Kullanıcı AI önerisini onaylayınca ürünü listeye ekle
   - İptal/duzeltme seçenekleri ekle
7. Saklama tavsiyesi üretme kuralını bağla:
   - AI’dan gelen veya kurallı bir haritadan türetilen `storageAdvice`
8. Hata yönetimi ekle:
   - AI başarısız / düşük güven skoru -> kullanıcıya anlaşılır mesaj
9. Loglama/izleme ekle:
   - AI çağrı süresi, hata türleri, talep başına sonuç
10. Performans testi:
   - Fotoğraf yüklemesinden ürün kaydına kadar hedef süreyi takip et (PRD: 10 sn altında)

## Faz 3: AI Şef (Tarif öneri) sistemi

1. “AI Şef” ekranını tasarla:
   - Mevcut envanteri girdi olarak kullan
   - Seçilebilir filtreler (tarihi yaklaşanlar, tercih edilen diyet vb. opsiyonel)
2. Backend’de tarif öneri endpoint’i ekle:
   - `POST /recipes/ai-chef` (envanter -> tarif önerileri)
3. Tarif çıktısı şemasını tanımla:
   - `recipeTitle`, `ingredients`, `steps`, `servings`, `calories` (varsa)
4. Envanterden “uygun malzeme eşleştirme” mantığını ekle:
   - Opsiyonel olarak “malzeme uyumu” skorla
5. AI prompt’u iyileştir:
   - Tarifin malzeme uyumlu ve uygulanabilir olmasını sağlayacak yönergeler
6. Kullanıcı etkileşimini ekle:
   - Tarif detayını göster
   - (opsiyonel) “Onayla ve stok düş” seçeneği
7. Stok güncelleme opsiyonunu uygula (eğer Faz 3 kapsamına dahil edilecekse):
   - Kullanılan malzemeleri envanterden düş
   - Malzeme birim uyumsuzluğu için basit dönüştürme stratejisi belirle
8. UI’da son kullanıcı deneyimini tamamla:
   - Yükleme durumları (spinner), hata mesajları, boş envanter senaryosu
9. Başarı kriterlerini doğrula:
   - Hız (PRD metrikleriyle ölç)
   - AI tanıma isabet oranı (pratik test setiyle yaklaş)
10. Geliştirme için küçük bir test planı yaz:
   - Envanter listeleme testi
   - AI giriş onaylama testi
   - Tarif üretme testi

## Cross-cutting (Tüm Fazlar İçin)

1. Ortam değişkenleri yönetimi:
   - AI API anahtarları, DB connection stringleri (sekretleri repo’ya koyma)
2. Tip/şema doğrulaması:
   - Backend’de request/response validation
3. Basit e2e senaryoları:
   - Manuel ürün ekle
   - AI girişten onayla
   - AI Şef’ten tarif al
4. Dokümantasyon:
   - Kurulum adımları
   - API dokümantasyonu (OpenAPI/Swagger varsa)

