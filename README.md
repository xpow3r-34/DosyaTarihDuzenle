# Dosya Tarih Düzenle

**Sürüm:** 1.3.2  
**Platform:** Windows 10/11  
**Gereksinim:** Python 3.10 veya üzeri.

Dosyaların oluşturulma, değiştirilme ve son erişim zamanlarını toplu olarak ayarlar. Dosya sırası, her dosyaya atanacak zamanı belirler.

## Contributors

- [xpow3r-34](https://github.com/xpow3r-34)

## Başlatma

`DosyaTarihDuzenle.bat` dosyasına çift tıklayın. Gerekli Pillow ve tkinterdnd2 paketleri eksikse başlatıcı bunları `requirements.txt` dosyasından kurar. Paket kurulumu için internet bağlantısı gerekir. Elle başlatmak için:

```powershell
python -m pip install -r requirements.txt
python app.py
```

## Kullanım

1. Tarih alanında gün, ay ve yılı; saat alanında saat, dakika ve saniyeyi ayrı ayrı metin kutularına girin. Nokta ve iki nokta ayraçları sabittir. Örnek: `06.11.2026` ve `23:23:00`.
2. Küçük resim boyutunu artış biriminin yanındaki slider ile 32–128 piksel aralığında ayarlayın.
3. Artış birimini seçin:
   - **Saniye:** her sıradaki dosyada bir saniye artar.
   - **Dakika:** her sıradaki dosyada bir dakika artar; saniye değeri sabit kalır.
4. Oluşturulma, değiştirilme ve son erişim alanlarından güncellenecek olanları seçin.
5. Dosyaları Windows Gezgini'nden listeye sürükleyip bırakın veya **Dosya ekle…** düğmesini kullanın.
6. Sıralamayı seçili dosyalarla **Yukarı taşı** / **Aşağı taşı** düğmeleriyle düzenleyin. Hedef tarih ve saat listede anında güncellenir.
7. **Tarihleri uygula** düğmesine basıp onaylayın.

Örneğin başlangıç `06.11.2026 23:23:00` ise saniye modunda ilk üç dosyanın zamanları `23:23:00`, `23:23:01`, `23:23:02` olur. Dakika modunda `23:23:00`, `23:24:00`, `23:25:00` olur. Tarihteki noktalar gün, ay ve yıl bilgisini ayırarak okunurluğu artırır.

## Görsel önizleme

PNG, JPEG, GIF, BMP, WebP ve TIFF görselleri listede küçük resimle gösterilir. Boyut seçimi listedeki satır yüksekliğini de ayarlar. Diğer dosya türleri dosya adıyla görünür.

## Kapsam ve notlar

- Tarihler yerel bilgisayar saat diliminde yorumlanır.
- Oluşturulma zamanı Windows dosya API'siyle ayarlanır. Kilitli veya yazma izni olmayan dosyalar hata listesinde gösterilir; işlem diğer dosyalarda sürer.
- Sürüm ve planlanan değişiklikler için [ROADMAP.md](ROADMAP.md), sürüm başına tamamlananlar için [CHANGELOG.md](CHANGELOG.md) dosyasına bakın.
