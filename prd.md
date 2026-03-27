# 📝 Product Requirements Document (PRD) - AI Based Kitchen Inventory

**Proje Adı:** AI Based Kitchen Inventory  
**Sürüm:** 1.0 (MVP)  
**Durum:** Planlama Aşaması  

---

## 1. Ürün Vizyonu (Vision)
**AI Based Kitchen Inventory**, evdeki gıda israfını teknoloji ile minimize etmeyi amaçlayan akıllı bir mutfak asistanıdır. Kullanıcıların zahmetli veri girişi süreçlerini yapay zeka (AI) ile kolaylaştırarak, mutfaklarındaki envanteri anlık olarak takip etmelerini ve ellerindeki malzemeleri en verimli şekilde değerlendirmelerini sağlar.

---

## 2. Temel Kullanıcı Senaryoları (User Stories)
* **Senaryo 1:** Yeni alışveriş yapan bir kullanıcı, ürünlerin fotoğrafını çekerek sisteme saniyeler içinde tanıtır.
* **Senaryo 2:** Kullanıcı buzdolabını açmadan telefonundan hangi ürünün ne kadar kaldığını ve bozulmasına kaç gün olduğunu kontrol eder.
* **Senaryo 3:** Akşam yemeği için fikri olmayan kullanıcı, "AI Şef" modülünü kullanarak elindeki (özellikle tarihi yaklaşan) malzemelerle yapılabilecek tarifler alır.

---

## 3. Fonksiyonel Gereksinimler (Functional Requirements)

### 3.1. Ürün Kayıt Modülü (AI Entry)
* **Görsel Tanıma:** Kullanıcı tarafından yüklenen fotoğraftaki nesne (meyve, sebze, paketli gıda vb.) AI tarafından tanımlanmalıdır.
* **Otomatik Veri Atama:** AI; ürün adı, miktar tahmini ve saklama koşullarına bağlı "Tahmini Tüketim Ömrü" bilgilerini üretmelidir.
* **Manuel Onay:** Kullanıcı, AI'nın ürettiği bu verileri kontrol edip onaylayabilmelidir.

### 3.2. Envanter Yönetim Paneli (Dashboard)
* **Listeleme:** Kayıtlı tüm ürünler; isim, miktar ve kalan gün sayısı ile listelenmelidir.
* **Saklama Tavsiyesi:** Her ürün için AI tabanlı "En İyi Saklama Yöntemi" bilgisi (buzdolabı, karanlık yer vb.) görüntülenmelidir.
* **Görsel Uyarı:** Son tüketim tarihi yaklaşan ürünler (örneğin son 2 gün) kritik renklerle (Kırmızı/Turuncu) vurgulanmalıdır.

### 3.3. AI Tarif Asistanı (Smart Recipes)
* **Envanter Analizi:** Sistemdeki mevcut ürünleri girdi olarak almalıdır.
* **Reçete Oluşturma:** Kullanıcıya eldeki malzemelerle hazırlanabilecek, porsiyon ve kalori bilgisi içeren yemek tarifleri sunmalıdır.
* **Stok Güncelleme:** (İsteğe bağlı) Kullanıcı tarifi onayladığında, kullanılan malzemeler envanterden düşülmelidir.

---

## 4. Teknik Gereksinimler (Technical Stack)
* **Frontend:** React.js veya Next.js (Hızlı ve modern bir web arayüzü için).
* **Backend:** Python (Flask/FastAPI) veya Node.js (AI API entegrasyonu için ideal).
* **Database:** Firebase veya PostgreSQL (Ürün verilerini saklamak için).
* **AI Engine:** Groq API (Llama Vision) (Görüntü işleme ve metin üretimi için).

---

## 5. Başarı Kriterleri (Success Metrics)
* Kullanıcının fotoğraf yüklemesinden ürünün listeye eklenmesine kadar geçen sürenin **10 saniyenin altında** olması.
* AI'nın nesne tanıma isabet oranının minimum **%80** olması.
* Kullanıcının elindeki malzemelerle üretilen tariflerin "uygulanabilir" ve "malzeme uyumlu" olması.

---

## 6. Yol Haritası (Roadmap)
* **Faz 1:** Temel envanter listeleme ve manuel ekleme.
* **Faz 2:** AI ile fotoğraftan ürün tanıma entegrasyonu.
* **Faz 3:** AI Şef (Tarif öneri) sisteminin devreye alınması.