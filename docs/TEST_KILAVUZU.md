# Test Kılavuzu - Open Textile Intelligence

Bu kılavuz, kamera modu implementasyonunun doğru çalıştığını doğrulamak için adım adım test sürecini açıklar.

---

## 🧪 Test Süreci Genel Bakış

1. **Hazırlık**: Gereksinimleri yükle ve kamera bağlantısını doğrula
2. **Kamera Testi**: Standalone test scriptini çalıştır
3. **Simülasyon Modu Testi**: Demo modunu doğrula
4. **Kamera Modu Testi**: Gerçek kamera girişini doğrula
5. **Mod Değiştirme Testi**: Güvenli geçişleri test et
6. **Kaynak Yönetimi Testi**: Kamera serbest bırakma işlemini doğrula

---

## 📋 Adım 1: Hazırlık

### Gereksinimleri Yükle

```bash
cd Open-Textile-Intelligence
pip install -r requirements.txt
```

**Beklenen Çıktı:**
```
Successfully installed:
- PySide6
- opencv-python
- numpy
- rich
```

### Webcam Bağlantısını Kontrol Et

**Windows:**
1. Kamera Uygulaması'nı aç (Windows + Search → "Camera")
2. Webcam görüntüsünün göründüğünü doğrula
3. Kamera Uygulaması'nı kapat (önemli: başka uygulama kamerayı kullanmasın)

**Alternatif:**
Kamera izinlerini kontrol et:
- Windows Ayarlar → Gizlilik → Kamera
- "Uygulamaların kameraya erişmesine izin ver" → AÇIK

---

## 🧪 Adım 2: Kamera Testi (Standalone)

Ana uygulamayı çalıştırmadan ÖNCE kamera bağlantısını test edin.

### Test Scripti Çalıştır

```bash
python desktop_app/test_camera.py
```

### ✅ Başarı Durumu

Şu çıktıyı görmelisiniz:

```
📦 OpenCV Versiyonu: 4.x.x

🎥 Kamera Testi Başlatılıyor...
📍 Test edilen kamera indeksi: 0
--------------------------------------------------
✅ Kamera başarıyla açıldı!
✅ Kare başarıyla okundu!

📊 Kamera Bilgileri:
   - Çözünürlük: 640 x 480
   - Kanal Sayısı: 3
   - Format: BGR

⏱️  FPS Testi (5 kare)...
   - Ortalama FPS: 29.85

🔍 Tespit Algoritması Testi...
   - Kenar Yoğunluğu: 0.0823
   - Bulanıklık Ölçüsü (Laplacian Var): 127.45

==================================================
✅ KAMERA TESTİ BAŞARILI!
==================================================
```

**➡️ Başarılıysa:** Adım 3'e geçin

### ❌ Hata Durumu

**Hata: "Kamera açılamadı"**

Çözüm adımları:
1. Farklı kamera indeksi deneyin:
   ```bash
   python desktop_app/test_camera.py 1
   ```

2. Tüm kameraları tarayın:
   ```bash
   python desktop_app/test_camera.py scan
   ```

3. Başka uygulama kamerayı kullanıyor olabilir:
   - Zoom, Teams, Skype gibi uygulamaları kapatın
   - Tarayıcı sekmelerini kontrol edin (kamera kullanan siteler)

4. Kamera izinlerini kontrol edin (yukarıdaki talimatlar)

**Hata: "Kare okunamadı"**

Çözüm adımları:
1. USB kablosunu çıkarıp tekrar takın
2. Bilgisayarı yeniden başlatın
3. Farklı bir USB portu deneyin

---

## 🧪 Adım 3: Simülasyon Modu Testi

Ana uygulamayı başlatın ve simülasyon modunu test edin.

### Uygulamayı Başlat

```bash
python desktop_app/main.py
```

### Test Adımları

1. **Uygulama Başlangıcını Doğrula**
   - ✅ Pencere açılıyor
   - ✅ Başlık: "Open Textile Intelligence – Real-Time Inspection System"
   - ✅ Mod seçici görünüyor: "🔧 Çalışma Modu: [SİMÜLASYON MODU ▼]"
   - ✅ Durum etiketi: "📍 AKTIF: SİMÜLASYON" (turuncu arka plan)

2. **Varsayılan Mod Kontrolü**
   - ✅ Varsayılan mod: "SİMÜLASYON MODU – Fiziksel Giriş Yok"
   - ✅ Kamera görüntüsü panelinde: "Kamera Modu: KAPALI"
   - ✅ FPS göstergesi: "--"

3. **Taramayı Başlat**
   - 🖱️ "Taramayı Başlat" butonuna tıkla
   - ✅ Kalibrasyon çubuğu 0% → 100% ilerliyor
   - ✅ Tarama ilerleme çubuğu artıyor
   - ✅ Tespit tablosuna satırlar ekleniyor
   - ✅ Kare ID'leri: "SIM-10001", "SIM-10002", vb.
   - ✅ Bazı satırlarda "KUSUR" durumu var (kırmızı)
   - ✅ İstatistikler güncelleniyor (Taranan Yard, Bulunan Kusur, Verimlilik)

4. **Tarama Tamamlanması**
   - ✅ İlerleme çubuğu 100% oldu
   - ✅ Buton tekrar "Taramayı Başlat" oldu
   - ✅ Mod seçici tekrar etkinleştirildi

### ✅ Başarı Kriteri

- Simülasyon modu yapay kusurlar üretiyor
- Kamera AÇILMIYOR (kamera görüntüsü paneli boş kalıyor)
- FPS göstergesi "--" (kare hızı yok)
- Tespit tablosu doluyor

---

## 🧪 Adım 4: Kamera Modu Testi

Gerçek kamera girişini test edin.

### Test Adımları

1. **Modu Değiştir**
   - 🖱️ Mod seçici açılır menüsüne tıkla
   - 🖱️ "GERÇEK KAMERA MODU – Canlı Giriş" seçeneğini seç
   - ✅ Durum etiketi: "📍 AKTIF: GERÇEK KAMERA" (yeşil arka plan)
   - ✅ Kamera görüntüsü panelinde hala "Kamera Modu: KAPALI" (henüz tarama başlamadı)

2. **Kamera Taramasını Başlat**
   - 🖱️ "Taramayı Başlat" butonuna tıkla
   - ✅ **ÖNEMLİ**: Kamera şimdi açılmalı
   - ✅ Kamera görüntüsü panelinde CANLI VIDEO AKIŞI görünüyor
   - ✅ FPS göstergesi gerçek değer gösteriyor (örn: "28.5", "30.2")
   - ✅ Kare ID'leri: "CAM-00001", "CAM-00002", vb.
   - ✅ Tespit tablosuna sadece GERÇEK tespitler ekleniyor (yapay değil)

3. **Canlı Video Doğrulaması**
   - ✅ Kameranın önünde hareket edin → video güncelleniyor
   - ✅ Elinizi kameranın önünde sallayın → görünüyor
   - ✅ Video akışı donmuyor

4. **FPS Doğrulaması**
   - ✅ FPS değeri dinamik olarak güncelleniyor
   - ✅ Tipik değerler: 25-30 FPS (sistem performansına bağlı)

5. **Tespit Mantığı Doğrulaması**
   - ✅ Tespit tablosu güncellenmeye devam ediyor
   - ✅ Kusur bulunursa "KUSUR" durumu gösteriliyor
   - ✅ Kusur tipi: "Dokuma Hatası (tespit: kenar yoğunluğu)" veya "Bulanık Alan (tespit: düşük varyans)"
   - ⚠️ NOT: Şu anki tespit mantığı GEÇİCİ (placeholder CV logic)

6. **Tarama Tamamlanması**
   - ✅ 10 saniye sonra tarama bitiyor
   - ✅ Kamera OTOMATIK KAPANIYOR
   - ✅ Kamera görüntüsü paneli boşalıyor
   - ✅ FPS göstergesi "--" oluyor
   - ✅ Mod seçici tekrar etkinleştirildi

### ✅ Başarı Kriteri

- Kamera sadece "Taramayı Başlat" butonuna basıldığında açılıyor
- Canlı video akışı sorunsuz çalışıyor
- FPS göstergesi gerçek zamanlı güncelleniyor
- Tespit tablosuna gerçek analiz sonuçları ekleniyor
- Tarama bittiğinde kamera otomatik kapanıyor

### ❌ Olası Hatalar

**Hata: "Kamera açılamadı" mesajı**
- Başka uygulama kamerayı kullanıyor olabilir
- Adım 2'deki kamera testini tekrar çalıştırın
- Kamera izinlerini kontrol edin

**Hata: Video donuyor**
- Sistem performansı yetersiz olabilir
- `camera_manager.py:84` satırında `time.sleep(0.033)` değerini artırın (örn: 0.05)

**Hata: FPS çok düşük (<15)**
- Yüksek çözünürlük sorun yaratıyor olabilir
- Sisteminizin CPU/bellek kullanımını kontrol edin

---

## 🧪 Adım 5: Mod Değiştirme Testi

Güvenli mod geçişlerini test edin.

### Test Senaryoları

#### Senaryo A: Tarama Sırasında Mod Değiştirme (ÖNEMLİ)

1. **Simülasyon modunda tarama başlat**
   - 🖱️ Mod: Simülasyon
   - 🖱️ "Taramayı Başlat" tıkla
   - ⏱️ Tarama devam ederken...

2. **Mod değiştirmeyi dene**
   - 🖱️ Mod seçici açılır menüsüne tıkla
   - 🖱️ "GERÇEK KAMERA MODU" seçmeye çalış
   - ✅ **BEKLENEN**: Mod DEĞİŞMEMELİ
   - ✅ Durum çubuğunda uyarı: "⚠️ Tarama devam ederken mod değiştirilemez!"
   - ✅ Mod seçici otomatik olarak eski moda (Simülasyon) geri dönmeli

3. **Tarama bitene kadar bekle**
   - ✅ Tarama tamamlandı
   - ✅ Mod seçici tekrar etkinleştirildi

4. **Şimdi mod değiştir**
   - 🖱️ Mod seçici → "GERÇEK KAMERA MODU"
   - ✅ Mod başarıyla değişti
   - ✅ Durum etiketi yeşil oldu

#### Senaryo B: Kamera Modundan Simülasyona Geçiş

1. **Kamera modunda tarama başlat**
   - 🖱️ Mod: Gerçek Kamera
   - 🖱️ "Taramayı Başlat" tıkla
   - ⏱️ Kamera açılıyor, video akışı başladı

2. **Taramayı durdur**
   - 🖱️ "Taramayı Durdur" butonuna tıkla
   - ✅ Kamera HEMEN kapanmalı
   - ✅ Video akışı durmalı
   - ✅ Mod seçici etkinleştirilmeli

3. **Simülasyon moduna geç**
   - 🖱️ Mod seçici → "SİMÜLASYON MODU"
   - ✅ Mod başarıyla değişti
   - ✅ Durum etiketi turuncu oldu

4. **Simülasyon taraması başlat**
   - 🖱️ "Taramayı Başlat" tıkla
   - ✅ Kamera AÇILMAMALI
   - ✅ Yapay kusur üretimi başlamalı

### ✅ Başarı Kriteri

- Tarama sırasında mod değiştirme ENGELLENİYOR
- Mod değişikliği sadece IDLE durumunda mümkün
- Mod değiştiğinde önceki kamera kaynakları serbest bırakılıyor

---

## 🧪 Adım 6: Kaynak Yönetimi Testi

Kamera kaynaklarının doğru şekilde serbest bırakıldığını doğrulayın.

### Test Adımları

#### Test A: Tarama Sırasında Pencereyi Kapatma

1. **Kamera modunda tarama başlat**
   - 🖱️ Mod: Gerçek Kamera
   - 🖱️ "Taramayı Başlat" tıkla
   - ✅ Kamera açıldı, video akışı başladı

2. **Pencereyi kapat (tarama devam ederken)**
   - 🖱️ Sağ üst köşede [X] butonuna tıkla
   - ✅ Uygulama HEMEN kapanmalı
   - ✅ Hata mesajı OLMAMALI
   - ✅ Python process sonlanmalı

3. **Kamera serbest bırakıldı mı kontrol et**
   - Uygulamayı tekrar başlat: `python desktop_app/main.py`
   - 🖱️ Kamera modunu seç
   - 🖱️ "Taramayı Başlat" tıkla
   - ✅ Kamera başarıyla açılmalı (serbest bırakılmış demektir)

#### Test B: Çoklu Tarama Döngüsü

1. **Aynı oturumda 3 kez tarama yap**
   - Tarama 1: Kamera modu → Başlat → Tamamla
   - Tarama 2: Kamera modu → Başlat → Tamamla
   - Tarama 3: Kamera modu → Başlat → Tamamla

2. **Her taramada kontrol et**
   - ✅ Kamera her seferinde açılıyor
   - ✅ Video akışı sorunsuz
   - ✅ FPS stabil
   - ✅ Bellek sızıntısı yok (Task Manager'da kontrol et)

#### Test C: Mod Geçiş Döngüsü

1. **Modlar arası geçiş yap**
   - Simülasyon → Başlat → Tamamla → Mod değiştir
   - Kamera → Başlat → Tamamla → Mod değiştir
   - Simülasyon → Başlat → Tamamla → Mod değiştir
   - Kamera → Başlat → Tamamla

2. **Her geçişte kontrol et**
   - ✅ Kamera doğru zamanda açılıp kapanıyor
   - ✅ Hiçbir kaynak sızıntısı yok
   - ✅ UI yanıt veriyor

### ✅ Başarı Kriteri

- Uygulama kapatıldığında kamera otomatik serbest bırakılıyor
- Çoklu tarama döngülerinde kaynak sızıntısı yok
- Mod geçişlerinde kamera düzgün açılıp kapanıyor

---

## 📊 Test Sonuçları Formu

Her test adımını tamamladıktan sonra işaretleyin:

### Adım 2: Kamera Testi
- [ ] Standalone test scripti başarılı
- [ ] Kamera bilgileri doğru gösteriliyor
- [ ] FPS hesaplaması çalışıyor
- [ ] Tespit algoritması testi geçti

### Adım 3: Simülasyon Modu
- [ ] Varsayılan mod doğru
- [ ] Yapay kusur üretimi çalışıyor
- [ ] Kamera açılmıyor
- [ ] FPS göstergesi "--"
- [ ] Kare ID formatı: SIM-XXXXX

### Adım 4: Kamera Modu
- [ ] Kamera sadece "Taramayı Başlat" ile açılıyor
- [ ] Canlı video akışı görünüyor
- [ ] FPS göstergesi gerçek değer gösteriyor
- [ ] Kare ID formatı: CAM-XXXXX
- [ ] Tespit mantığı çalışıyor
- [ ] Tarama bitince kamera kapanıyor

### Adım 5: Mod Değiştirme
- [ ] Tarama sırasında mod değiştirme engelleniyor
- [ ] Uyarı mesajı gösteriliyor
- [ ] IDLE durumunda mod değiştirme çalışıyor
- [ ] Mod etiketleri doğru güncelleniyor

### Adım 6: Kaynak Yönetimi
- [ ] Pencere kapatma kamerayı serbest bırakıyor
- [ ] Çoklu tarama döngüsü sorunsuz
- [ ] Mod geçişlerinde kaynak sızıntısı yok
- [ ] Bellek kullanımı stabil

---

## 🐛 Sorun Raporlama

Herhangi bir test başarısız olursa, aşağıdaki bilgileri toplayın:

### Hata Bilgileri

```
Test Adımı: [Adım numarası ve adı]
Hata Mesajı: [Tam hata mesajı]
Beklenen Davranış: [Ne olmalıydı]
Gerçekleşen Davranış: [Ne oldu]
Sistem Bilgisi:
  - İşletim Sistemi: Windows 10/11
  - Python Versiyonu: [python --version]
  - OpenCV Versiyonu: [test_camera.py çıktısından]
  - Webcam Modeli: [Kamera adı]
```

### Log Dosyası

Hata oluşursa, console çıktısını kaydedin:

```bash
python desktop_app/main.py > test_log.txt 2>&1
```

---

## ✅ Tüm Testler Başarılı Olduğunda

Tebrikler! Kamera modu implementasyonu başarıyla doğrulandı.

### Sonraki Adımlar

1. **Üretim Kullanımı**
   - Uygulamayı gerçek kumaş muayene ortamında kullanın
   - Tespit doğruluğunu değerlendirin

2. **ML Model Entegrasyonu** (Gelecek)
   - `camera_manager.py:90` → `_analyze_frame_for_defects()` fonksiyonunu değiştirin
   - Geçici CV mantığını eğitilmiş ML modeli ile değiştirin

3. **Kalibrasyon**
   - Kenar yoğunluğu eşiklerini ayarlayın
   - Bulanıklık ölçüm parametrelerini optimize edin

4. **Performans Optimizasyonu**
   - GPU hızlandırma ekleyin (CUDA)
   - Çoklu kamera desteği

---

## 📚 İlgili Dokümantasyon

- **KAMERA_MODU_KILAVUZU.md** - Kullanıcı kılavuzu
- **IMPLEMENTATION_SUMMARY.md** - Teknik detaylar
- **requirements.txt** - Gerekli paketler

---

**Son Güncelleme:** 2025-12-26
**Versiyon:** 1.0
**Durum:** Kamera Modu Implementasyonu - Test Aşaması
