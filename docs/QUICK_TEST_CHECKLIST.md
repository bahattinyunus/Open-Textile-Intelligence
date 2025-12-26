# Hızlı Test Kontrol Listesi

Kamera modu implementasyonunu hızlıca test etmek için bu listeyi kullanın.

## 🚀 Hızlı Başlangıç

```bash
# 1. Gereksinimleri yükle
pip install -r requirements.txt

# 2. Kamera testini çalıştır
python desktop_app/test_camera.py

# 3. Uygulamayı başlat
python desktop_app/main.py
```

---

## ✅ Kritik Kontrol Noktaları

### 1️⃣ Başlangıç Kontrolü (30 saniye)
- [ ] Uygulama penceresi açıldı
- [ ] Mod seçici görünüyor: "SİMÜLASYON MODU" varsayılan
- [ ] Durum etiketi turuncu: "📍 AKTIF: SİMÜLASYON"

### 2️⃣ Simülasyon Modu (1 dakika)
- [ ] "Taramayı Başlat" tıklandı
- [ ] Kare ID'leri: SIM-10001, SIM-10002...
- [ ] Kamera AÇILMIYOR (panel boş)
- [ ] FPS: "--"

### 3️⃣ Kamera Modu (2 dakika)
- [ ] Mod seçici → "GERÇEK KAMERA MODU"
- [ ] Durum etiketi yeşil: "📍 AKTIF: GERÇEK KAMERA"
- [ ] "Taramayı Başlat" tıklandı
- [ ] **CANLI VIDEO AKIŞI GÖRÜNÜYOR** ✨
- [ ] FPS: gerçek değer (25-30)
- [ ] Kare ID'leri: CAM-00001, CAM-00002...

### 4️⃣ Mod Değiştirme Güvenliği (1 dakika)
- [ ] Tarama sırasında mod değiştirme denendi
- [ ] **ENGELLENDI** ✅
- [ ] Uyarı mesajı gösterildi

### 5️⃣ Kaynak Yönetimi (30 saniye)
- [ ] Tarama bitti → Kamera KAPANDI
- [ ] Pencere kapatıldı → Hata YOK
- [ ] Tekrar başlatıldı → Kamera AÇILDI

---

## ❌ Kritik Hatalar

Aşağıdaki durumlardan biri olursa DURDURUN ve hata raporu oluşturun:

1. **Kamera açılamıyor** → `desktop_app/test_camera.py` çalıştırın
2. **Video donuyor** → Sistem performansı yetersiz
3. **Mod değişirken crash** → Kod hatası olabilir
4. **Kamera kapanmıyor** → Kaynak sızıntısı var

---

## 🎯 5 Dakikada Test

**Toplam Süre:** 5 dakika

1. **[0:00-0:30]** Kamera testini çalıştır
2. **[0:30-1:30]** Simülasyon modunu test et
3. **[1:30-3:30]** Kamera modunu test et
4. **[3:30-4:30]** Mod değiştirmeyi test et
5. **[4:30-5:00]** Pencereyi kapat ve tekrar aç

**BAŞARI:** Tüm adımlar sorunsuz geçti ✅

---

## 📞 Yardım

Detaylı test talimatları için:
```
TEST_KILAVUZU.md
```

Kullanıcı kılavuzu için:
```
KAMERA_MODU_KILAVUZU.md
```
