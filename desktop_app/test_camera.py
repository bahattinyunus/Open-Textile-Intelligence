"""
Standalone camera test script for Open Textile Intelligence.
Tests if OpenCV can access the webcam before running the full application.

Run this BEFORE launching the main application to verify camera setup.
"""

import cv2
import sys

def test_camera(camera_index=0):
    """
    Test if camera can be opened and frames can be captured.

    Args:
        camera_index: Camera device index (default: 0 for primary webcam)

    Returns:
        bool: True if camera works, False otherwise
    """
    print(f"🎥 Kamera Testi Başlatılıyor...")
    print(f"📍 Test edilen kamera indeksi: {camera_index}")
    print("-" * 50)

    # Try to open camera
    cap = cv2.VideoCapture(camera_index)

    if not cap.isOpened():
        print(f"❌ HATA: Kamera açılamadı (indeks: {camera_index})")
        print("\n🔧 Olası Çözümler:")
        print("1. Webcam'in bilgisayara bağlı olduğundan emin olun")
        print("2. Başka bir uygulama kamerayı kullanıyor olabilir (Zoom, Teams, vb.)")
        print("3. Windows Ayarlar > Gizlilik > Kamera izinlerini kontrol edin")
        print("4. Farklı bir kamera indeksi deneyin: python test_camera.py 1")
        return False

    print(f"✅ Kamera başarıyla açıldı!")

    # Try to read a frame
    ret, frame = cap.read()

    if not ret:
        print(f"❌ HATA: Kare okunamadı")
        print("\n🔧 Olası Çözümler:")
        print("1. Kamera bağlantısını kontrol edin")
        print("2. USB kablosunu çıkarıp tekrar takın")
        print("3. Bilgisayarı yeniden başlatın")
        cap.release()
        return False

    # Display frame information
    height, width, channels = frame.shape
    print(f"✅ Kare başarıyla okundu!")
    print(f"\n📊 Kamera Bilgileri:")
    print(f"   - Çözünürlük: {width} x {height}")
    print(f"   - Kanal Sayısı: {channels}")
    print(f"   - Format: {'BGR' if channels == 3 else 'Grayscale'}")

    # Test frame rate
    print(f"\n⏱️  FPS Testi (5 kare)...")
    import time
    start_time = time.time()
    frame_count = 0

    for i in range(5):
        ret, frame = cap.read()
        if ret:
            frame_count += 1

    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time if elapsed_time > 0 else 0

    print(f"   - Ortalama FPS: {fps:.2f}")

    # Test defect detection logic (placeholder)
    print(f"\n🔍 Tespit Algoritması Testi...")
    import numpy as np

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = np.count_nonzero(edges) / (edges.shape[0] * edges.shape[1])
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()

    print(f"   - Kenar Yoğunluğu: {edge_density:.4f}")
    print(f"   - Bulanıklık Ölçüsü (Laplacian Var): {laplacian_var:.2f}")

    # Release camera
    cap.release()

    print("\n" + "=" * 50)
    print("✅ KAMERA TESTİ BAŞARILI!")
    print("=" * 50)
    print("\n📌 Sonraki Adım:")
    print("   Uygulamayı çalıştırın: python desktop_app/main.py")
    print("   Mod seçici menüden 'GERÇEK KAMERA MODU' seçin")

    return True


def test_multiple_cameras():
    """Test multiple camera indices to find available cameras."""
    print("🔍 Mevcut Kameraları Tarama...")
    print("-" * 50)

    available_cameras = []

    for i in range(5):  # Test first 5 indices
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                available_cameras.append(i)
                print(f"✅ Kamera bulundu: indeks {i}")
            cap.release()

    if not available_cameras:
        print("❌ Hiç kamera bulunamadı!")
    else:
        print(f"\n📊 Toplam {len(available_cameras)} kamera bulundu: {available_cameras}")
        print(f"   Varsayılan kamera: indeks {available_cameras[0]}")

    return available_cameras


if __name__ == "__main__":
    # Check OpenCV installation
    print("📦 OpenCV Versiyonu:", cv2.__version__)
    print()

    # Parse camera index from command line
    camera_index = 0
    if len(sys.argv) > 1:
        try:
            camera_index = int(sys.argv[1])
        except ValueError:
            print("⚠️ Geçersiz kamera indeksi, varsayılan 0 kullanılıyor")

    # Run camera test
    if len(sys.argv) > 1 and sys.argv[1] == "scan":
        # Scan for all available cameras
        test_multiple_cameras()
    else:
        # Test specific camera
        success = test_camera(camera_index)

        if not success:
            print("\n🔧 Başka bir kamera denemek için:")
            print("   python desktop_app/test_camera.py 1")
            print("\n🔍 Tüm kameraları taramak için:")
            print("   python desktop_app/test_camera.py scan")
            sys.exit(1)
