# Yol Haritası

Bu dosya, Dosya Tarih Düzenle uygulamasındaki sürümleri ve planlanan değişiklikleri kaydeder. Sürümleme SemVer biçimindedir (`MAJOR.MINOR.PATCH`).

## v1.0.0 — İlk kullanılabilir sürüm (tamamlandı)

- Görsel Tkinter arayüzü ve Windows dosya zamanlarını yazma.
- Çoklu dosya seçme, listeleme, kaldırma ve temizleme.
- Başlangıç zamanından saniye bazında artış ve hedef zaman önizlemesi.
- Oluşturulma, değiştirilme ve son erişim alanlarını bağımsız seçme.
- Uygulama öncesi onay ve dosya bazında hata raporu.

## v1.1.0 — Sürükle bırak ve zaman sıralama (tamamlandı)

- Windows Gezgini'nden dosyaları listeye sürükleyip bırakma.
- Görsel dosyalar için küçük resim önizlemesi (PNG, JPEG, GIF, BMP, WebP, TIFF).
- Seçili dosyaları yukarı/aşağı taşıma; sıra değiştikçe hedef zamanları anında yenileme.
- Artış birimi seçimi: saniye veya dakika. Dakika modunda saniye bileşeni sabit kalır.
- Tarih giriş ve önizlemesinde noktalarla gün/ay/yıl ayracı.
- Pillow ve tkinterdnd2 bağımlılıkları ile eksik paketleri başlatıcıdan kurma.
- Sürümün `1.1.0` olarak güncellenmesi ve bu yol haritasının yenilenmesi.

## v1.2.0 — Tarih giriş ve küçük resim ayarları (tamamlandı)

- Tarih ve saat girişlerini ayrı alanlara bölme.
- Gün, ay, yıl, saat, dakika ve saniye alanlarının arasına değiştirilemeyen sabit ayraçlar ekleme.
- Küçük resim boyutunu arayüzden 32–128 piksel arasında ayarlama ve satır yüksekliğini seçime uydurma.
- Sürümü `1.2.0` olarak güncelleme; kullanım kılavuzu ve değişiklik günlüğünü eşitleme.

## v1.2.1 — Giriş alanı görünüm düzeltmesi (tamamlandı)

- Tarih ve saat girişlerini ok düğmeleri olmayan, ortalanmış metin kutularına dönüştürme.
- Giriş gruplarını görsel olarak belirginleştirme ve sabit ayraçların okunurluğunu artırma.
- Sürümü `1.2.1` olarak güncelleme.

## v1.3.0 — Ayarlar paneli düzeni (tamamlandı)

- Küçük resim boyutu seçimini açılır listeden slider kontrolüne dönüştürme.
- Slider'ı artış biriminin sağına, oluşturulma/değiştirilme/son erişim seçimlerini slider'ın sağına taşıma.
- Gereksiz açıklama satırını kaldırıp ayar alanında yer kazanma.
- Sürümü `1.3.0` olarak güncelleme.

## v1.3.1 — Slider görünümü (tamamlandı)

- Küçük resim boyutu slider'ını ttk yatay slider'a dönüştürerek uygulamanın genel temasıyla eşleştirme.
- Slider üzerindeki boyut değerini kaldırma; 16 piksel adımlı boyut seçimini koruma.
- Sürümü `1.3.1` olarak güncelleme.

## v1.3.2 — Slider değer kararlılığı (tamamlandı)

- Slider boyutunu dosya ekleme ve liste yenileme işleminden bağımsız hale getirme.
- Boyut önizlemesini slider bırakıldığında yenileme; slider değerinin uçlara sıçramasını önleme.
- Sürümü `1.3.2` olarak güncelleme.

## v1.4.0 — İşlem kontrolü (planlandı)

- İşlem günlüğünü dosyaya kaydetme ve sonuçları dışa aktarma.
- Hata veren dosyaları yeniden deneme.
- Kullanıcının belirlediği artış miktarını seçme (ör. 5 saniye veya 10 dakika).
- Mevcut zamanlarla hedef zamanları işlem öncesinde karşılaştırma.

## v2.0.0 — Dağıtım (planlandı)

- Windows için Python kurulumundan bağımsız çalıştırılabilir paket oluşturma.
- Sürüm ve güncelleme bilgisini arayüzde gösterme.
- Arayüz ölçekleme ve klavye erişilebilirliği iyileştirmeleri.

Planlanan özellikler henüz uygulamanın parçası değildir; tamamlandıklarında ilgili sürüm ve değişiklik günlüğü güncellenecektir.
