# Open Textile Intelligence - Masaüstü Uygulaması

## Windows İçin Yerel Masaüstü Uygulaması

Bu, PySide6 (Python için Qt) ile oluşturulmuş **gerçek bir yerel masaüstü uygulamasıdır**, web uygulaması DEĞİLDİR.

## Özellikler

- **Yerel Windows Uygulaması**: Yerel bir pencere olarak açılır, tarayıcı gerekmez
- **Gerçek Zamanlı Tespit**: Yumuşak animasyonlarla canlı güncellemeler
- **Koyu Endüstriyel Tema**: Profesyonel izleme arayüzü
- **Thread Güvenli**: Arka plan tespiti UI'ı engellemez
- **PyInstaller Hazır**: Bağımsız .exe olarak paketlenebilir

## Kurulum

### 1. Bağımlılıkları Yükleyin

```bash
cd Open-Textile-Intelligence
pip install -r requirements.txt
```

Gerekli paketler:
- `PySide6` - Python için Qt framework
- `rich` - Terminal çıktısı (opsiyonel)
- `numpy` - Sayısal işlemler

### 2. Uygulamayı Çalıştırın

```bash
cd desktop_app
python main.py
```

Uygulama penceresi hemen açılacaktır.

## Kullanım

1. **Tarama Süresini Ayarlayın**: Kaydırıcıyı kullanın (5-60 saniye)
2. **Taramayı Başlatın**: "▶ Taramayı Başlat" butonuna tıklayın
3. **Gerçek Zamanlı Tespiti İzleyin**: Kusurlar tespit edildikçe tabloda görünür
4. **İstediğiniz Zaman Durdurun**: Erken durdurmak için "⏹ Durdur" butonuna tıklayın

## Arayüz Bileşenleri

### Üst Metrikler
- **📏 Taranan Uzunluk**: Toplam taranan uzunluk (yarda)
- **⚠️ Tespit Edilen Kusur**: Tespit edilen kusur sayısı
- **✅ Verimlilik Oranı**: Verimlilik yüzdesi
- **🔄 Durum**: Mevcut sistem durumu

### İlerleme Çubukları
- **Sensör Kalibrasyonu**: Sensör kalibrasyon ilerlemesi
- **Kumaş Tarama İlerlemesi**: Kumaş tarama ilerlemesi

### Tespit Tablosu
Tespit edilen kusurların canlı akışı:
- Zaman damgası
- Kare numarası
- Durum göstergesi
- Kusur tipi (önem derecesine göre renkli)
- Güven yüzdesi

### Renk Kodlaması
- 🔴 **Kırmızı**: Kritik kusurlar (Delik, İplik Kopması)
- 🟡 **Sarı**: Uyarılar (Renk Uyuşmazlığı)
- 🟠 **Turuncu**: Orta seviye sorunlar (Leke, Dokuma Hatası)

## Mimari

```
desktop_app/
├── main.py                    # Giriş noktası
├── detection_manager.py       # Arka plan tespit thread'i
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # Ana pencere sınıfı
│   └── styles.py              # Koyu tema stilleri
└── BENIOKU.md                 # Bu dosya
```

### Thread Mimarisi

```
Ana Thread (UI)
    ↓
    Sinyaller/Slotlar
    ↓
Arka Plan Thread'i (DetectionManager)
    ↓
    FabricScanner (Tespit Mantığı)
```

## .exe Olarak Paketleme

### PyInstaller Kullanımı

```bash
pip install pyinstaller

# Basit paketleme
pyinstaller --onefile --windowed --name="OpenTextileIntelligence" main.py

# İkonlu gelişmiş paketleme
pyinstaller --onefile --windowed --icon=icon.ico --name="OpenTextileIntelligence" main.py
```

Çıktı: `dist/OpenTextileIntelligence.exe`

### Dağıtım

Oluşturulan .exe dosyası:
- Diğer Windows makinelerine kopyalanabilir
- Python kurulumu olmadan çalıştırılabilir
- Son kullanıcılara dağıtılabilir
- Ağ sürücülerine yerleştirilebilir

## Teknik Detaylar

### UI Framework
- **PySide6**: Python için resmi Qt bağlantıları
- **QMainWindow**: Ana uygulama penceresi
- **QTableWidget**: Tespit tablosu
- **QProgressBar**: İlerleme göstergeleri
- **QThread**: Arka plan işleme

### Gerçek Zamanlı Güncellemeler
- Tespit ayrı bir thread'de çalışır (DetectionManager)
- Qt Sinyalleri UI thread'i ile iletişim kurar
- Yeni satırlar kısa bir vurgulamayla canlandırılır
- En son tespite otomatik kaydırma

### Stillendirme
- Endüstriyel estetiğe sahip özel koyu tema
- Gradyan metrik kartları
- Kusur önem derecesine göre renklendirilmiş
- Okunabilirlik için yüksek kontrast

## Karşılaştırma: Web vs Masaüstü

| Özellik | Web (Streamlit) | Masaüstü (PySide6) |
|---------|----------------|-------------------|
| Tip | Tarayıcı tabanlı | Yerel pencere |
| Performans | İyi | Mükemmel |
| Çevrimdışı | Hayır | Evet |
| .exe Paketleme | Hayır | Evet |
| Sistem Entegrasyonu | Sınırlı | Tam |
| Başlangıç Zamanı | Yavaş | Hızlı |

## Geliştirme

### Yeni Özellikler Ekleme

1. **UI Değişiklikleri**: `ui/main_window.py` dosyasını düzenleyin
2. **Stillendirme**: `ui/styles.py` dosyasını değiştirin
3. **Tespit Mantığı**: `detection_manager.py` dosyasını güncelleyin
4. **Giriş Noktası**: `main.py` dosyasını yapılandırın

### Hata Ayıklama

Konsol çıktısı ile çalıştırın:
```bash
python main.py
```

Hata mesajları için terminali kontrol edin.

## Gelecek Geliştirmeler

- [ ] Tespit raporunu PDF'ye aktarma
- [ ] Tarama oturumlarını kaydetme/yükleme
- [ ] Gerçek kamera akışı entegrasyonu
- [ ] Çoklu dil desteği
- [ ] Sistem tepsisi entegrasyonu
- [ ] Otomatik güncelleme mekanizması

## Lisans

MIT Lisansı - Ana proje LİSANS dosyasına bakın

## Yazar

**Bahattin Yunus Çetin**
IT Mimarı
Trabzon, Türkiye

---

**Bu yerel bir masaüstü uygulamasıdır. Web sunucusu veya tarayıcı gerektirmez.**
