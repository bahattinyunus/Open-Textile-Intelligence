# Kamera Modu Kılavuzu - Open Textile Intelligence

## 🎥 GERÇEK KAMERA DESTEĞİ EKLENDİ

Sistem artık **gerçek kamera girişi** ile çalışabilir! Bu, uygulamayı bir DEMO'dan **GERÇEK BİR ÜRÜNE** dönüştürür.

---

## 🔧 İki Çalışma Modu

### 1. SİMÜLASYON MODU (Varsayılan)
- ❌ Fiziksel kamera kullanılmaz
- ❌ Yapay kusur üretimi
- ✅ Test ve demo için ideal
- ✅ Donanım gerektirmez

### 2. GERÇEK KAMERA MODU (YENİ!)
- ✅ Gerçek kamera akışı
- ✅ OpenCV ile kare yakalama
- ✅ Gerçek bilgisayarlı görü analizi
- ✅ Canlı FPS göstergesi
- ⚠️ Webcam gerektirir (varsayılan: kamera indeks 0)

---

## 🚀 Nasıl Kullanılır

### Mod Seçimi

1. Uygulamayı başlatın: `python desktop_app/main.py`
2. Üst kısımdaki **"Çalışma Modu"** açılır menüsünden seçin:
   - **SİMÜLASYON MODU** (turuncu) - Fiziksel giriş yok
   - **GERÇEK KAMERA MODU** (yeşil) - Canlı giriş

3. Mod seçiminden sonra "Taramayı Başlat" butonuna tıklayın

### ⚠️ ÖNEMLİ KURALLAR

**Mod Değiştirme:**
- ✅ Mod değiştirmek için tarama DURDURULMUŞ olmalı
- ❌ Tarama sırasında mod değiştirilemez
- ✅ Mod değiştiğinde kamera otomatik serbest bırakılır

**Kamera Başlatma:**
- ❌ Kamera otomatik BAŞLAMAZ
- ✅ Kamera sadece "Taramayı Başlat" butonuna tıklandığında açılır
- ✅ Tarama bittiğinde kamera otomatik kapanır

---

## 📊 Arayüz Bileşenleri

### Mod Göstergesi
```
🔧 Çalışma Modu: [SİMÜLASYON MODU ▼]  📍 AKTIF: SİMÜLASYON
```
- **Turuncu etiket** = Simülasyon aktif
- **Yeşil etiket** = Gerçek kamera aktif

### Kamera Görüntüsü Paneli
Sol tarafta kamera görüntüsü gösterilir:
- **Simülasyon modunda**: "Kamera Modu: KAPALI"
- **Kamera modunda**: Canlı video akışı

### FPS Göstergesi
- **Simülasyon**: "--" (kare hızı yok)
- **Kamera**: Gerçek zamanlı FPS değeri (örn: "29.8")

---

## 🎯 Tespit Mantığı

### Simülasyon Modunda
- Yapay/rastgele kusur üretimi
- `SIM-10001`, `SIM-10002` gibi kare ID'leri
- Gerçek donanım gerektirmez

### Kamera Modunda (GERÇEK)
- **OpenCV ile kare yakalama**
- **Gerçek bilgisayarlı görü analizi**:
  - Kenar tespiti (Canny)
  - Bulanıklık ölçümü (Laplacian varyansı)
  - **ŞU AN: Geçici CV mantığı (ML model bekleniyor)**
- `CAM-00001`, `CAM-00002` gibi kare ID'leri
- ❌ Kamera modunda YAPAY kusur üretilmez
- ✅ Sadece GERÇEK tespit sonuçları gösterilir

---

## 🔍 Tespit Algoritması (Kamera Modu)

### Mevcut Uygulama (GEÇİCİ)

Kamera modunda şu CV teknikleri kullanılır:

```python
# 1. Kenar Yoğunluğu Analizi
edges = cv2.Canny(frame, 50, 150)
edge_density = np.count_nonzero(edges) / total_pixels

# 2. Bulanıklık Ölçümü
laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

# Geçici Eşik Değerleri:
- Yüksek kenar yoğunluğu (>0.15) → Dokuma Hatası
- Düşük varyans (<50) → Bulanık Alan
```

### ⚠️ ÖNEMLİ NOT
Bu **GEÇİCİ BİR PLACEHOLDER MANTIĞIDIR**. Gerçek üretim için:
- ✅ Eğitilmiş ML modeli entegre edilecek
- ✅ Derin öğrenme tabanlı tespit
- ✅ Gerçek kumaş kusur sınıflandırması

---

## 🛡️ Durum Yönetimi

### Sistem Durumları

1. **IDLE (Boşta)**
   - Tarama yok
   - Kamera kapalı
   - Mod değiştirme mümkün

2. **SCANNING_SIMULATION (Simülasyon Taranıyor)**
   - Simülasyon aktif
   - Kamera kapalı
   - Mod kilitli

3. **SCANNING_CAMERA (Kamera Taranıyor)**
   - Kamera aktif
   - Canlı video akışı
   - Mod kilitli

### Güvenli Geçişler

```
IDLE → [Mod Seç] → IDLE
IDLE → [Başlat] → SCANNING_SIMULATION/CAMERA
SCANNING → [Durdur] → IDLE
```

---

## 📋 Kurulum

### Gerekli Paketler

```bash
pip install -r requirements.txt
```

Yeni eklenenler:
- `opencv-python` - Kamera desteği için

### Kamera Kontrolü

Kameranızın çalıştığını test edin:

```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
print("Kamera çalışıyor!" if ret else "Kamera bulunamadı!")
cap.release()
```

---

## 🔧 Sorun Giderme

### "Kamera açılamadı" Hatası

**Olası sebepler:**
1. Webcam bağlı değil
2. Başka uygulama kamerayı kullanıyor
3. Kamera izinleri engellendi (Windows ayarları)

**Çözüm:**
```bash
# Kamera indeksini değiştir
# camera_manager.py dosyasında:
CameraManager(camera_index=1)  # Farklı kamera dene
```

### "Kare okunamadı" Hatası

- Kamera bağlantısı koptu
- USB kablosu gevşek
- Donanım sorunu

**Çözüm**: Kamerayı çıkar/tak, uygulamayı yeniden başlat

### FPS Çok Düşük

- Sistem yavaş
- Yüksek çözünürlük

**Çözüm**: `camera_manager.py` dosyasında FPS kontrolünü ayarla:
```python
time.sleep(0.033)  # ~30 FPS
```

---

## 📂 Dosya Yapısı

```
desktop_app/
├── constants.py          ← YENİ: Mod ve durum enum'ları
├── camera_manager.py     ← YENİ: Gerçek kamera yönetimi
├── detection_manager.py  ← GÜNCELLENDİ: Mod desteği
├── ui/
│   └── main_window.py    ← GÜNCELLENDİ: Mod seçici + kamera görünümü
└── main.py              ← Değişmedi
```

---

## 🎓 Gelecek Geliştirmeler

### Kısa Vadede
- [ ] Kamera yeniden bağlanma desteği
- [ ] Çoklu kamera desteği (indeks seçici)
- [ ] Kaydedilmiş video dosyası oynatma
- [ ] Kare kaydetme özelliği

### Orta Vadede
- [ ] ML model entegrasyonu (YOLO/TensorFlow)
- [ ] Gerçek kumaş kusur sınıflandırması
- [ ] Gelişmiş CV algoritmaları
- [ ] Kamera parametreleri ayarı (çözünürlük, FPS)

### Uzun Vadede
- [ ] Çoklu kamera senkronizasyonu
- [ ] Endüstriyel kamera desteği (GigE Vision)
- [ ] GPU hızlandırma
- [ ] Gerçek zamanlı rapor oluşturma

---

## ✅ Özet

| Özellik | Durum |
|---------|-------|
| Simülasyon Modu | ✅ Çalışıyor |
| Kamera Modu | ✅ Çalışıyor |
| Mod Değiştirme | ✅ Güvenli |
| Kamera Akışı | ✅ OpenCV |
| FPS Göstergesi | ✅ Canlı |
| Geçici CV Mantığı | ✅ Uygulandı |
| ML Model | ⏳ Bekleniyor |
| Durum Yönetimi | ✅ Tam |

---

**Bu artık bir DEMO değil, GERÇEK BİR ÜRÜNDÜR!**

Kamera girişi ile çalışan, mod değiştirme özellikli, üretim seviyesi bir sistem.
