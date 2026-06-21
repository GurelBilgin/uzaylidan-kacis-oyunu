# Uzaylıdan Kaçış Oyunu

Bu proje, Python ve Tkinter kullanılarak geliştirilmiş basit bir harf tahmin oyunudur. Oyuncu, ekranda gizlenen cümleyi harf tahminleri yaparak bulmaya çalışır. Yanlış tahminlerde uzaylı oyuncuya yaklaşır; hata hakkı dolmadan cümle bulunursa oyun kazanılır.

Proje ilk hâlindeki tek dosyalı yapıdan çıkarılarak modüler, test edilebilir ve GitHub üzerinde daha düzenli görünecek bir Python proje yapısına dönüştürülmüştür.

## Özellikler

- Tkinter tabanlı masaüstü arayüz
- Harf tahmin etme mekanizması
- Gizli cümleleri `cumleler.txt` dosyasından okuma
- Her tahmin için süre sınırı
- Tuzak harflerde ekstra hata cezası
- Tek kullanımlık ipucu hakkı
- Kazanma ve kaybetme durumları
- Skorları kullanıcıya özel uygulama veri klasöründe saklama
- Oyun içi ses efektleri
- Uygulama ikonu
- Modüler ve test edilebilir oyun mantığı

## Proje Yapısı

```text
uzaylidan-kacis-oyunu/
├── README.md
├── pyproject.toml
├── .gitignore
├── src/
│   └── uzaylidan_kacis_oyunu/
│       ├── __init__.py
│       ├── game_logic.py
│       ├── gui.py
│       ├── main.py
│       ├── resources.py
│       ├── scoreboard.py
│       ├── sound.py
│       └── assets/
│           ├── app_icon.ico
│           ├── cumleler.txt
│           ├── correct.wav
│           ├── wrong.wav
│           ├── win.wav
│           └── lose.wav
└── tests/
    ├── test_game_logic.py
    └── test_scoreboard.py
```

## Kurulum

Python 3.10 veya üzeri önerilir.

```bash
python -m pip install -e .
```

Bu komut proje bağımlılıklarını kurar ve uygulamayı komut satırından çalıştırılabilir hâle getirir.

## Çalıştırma

Paket modülü üzerinden çalıştırmak için:

```bash
python -m uzaylidan_kacis_oyunu.main
```

Kurulumdan sonra kısa komutla çalıştırmak için:

```bash
uzaylidan-kacis
```

## Oynanış

1. Ana ekranda **Oyunu Başlat** butonuna basılır.
2. Gizlenen cümleyi bulmak için tek harflik tahminler yapılır.
3. Doğru tahminlerde ilgili harfler açılır.
4. Yanlış tahminlerde hata sayısı artar ve uzaylı oyuncuya yaklaşır.
5. `x`, `z`, `j` ve `q` harfleri tuzak harflerdir; yanlış tahmin edilirse iki hata cezası verir.
6. Her tahmin için süre sınırı vardır. Süre dolarsa hata sayısı artar.
7. Oyuncunun bir kez ipucu alma hakkı vardır.
8. Cümle tamamlanırsa oyun kazanılır; hata hakkı dolarsa oyun kaybedilir.


## Skor Dosyasının Konumu

Oyun skorları EXE dosyasının bulunduğu klasöre yazılmaz. Kullanıcı oyunu doğrudan indirip çalıştırdığında `dist/` veya indirme klasöründe `scores.txt` oluşmaması için skor dosyası kullanıcıya özel uygulama veri klasöründe tutulur.

Windows için varsayılan konum:

```text
%APPDATA%\UzaylidanKacisOyunu\scores.txt
```

Bu sayede uygulama `Program Files`, masaüstü veya indirilenler klasörü gibi farklı yerlerden çalıştırılsa bile skor kayıtları düzenli ve güvenli bir konumda saklanır.

## Testler

Projedeki testleri çalıştırmak için:

```bash
python -m unittest discover -s tests -v
```

Testler, oyun mantığının arayüzden bağımsız olarak doğru çalıştığını kontrol eder.

## Windows EXE Oluşturma

Windows kullanıcıları için uygulama PyInstaller ile tek dosyalık `.exe` hâline getirilebilir.

Önce PyInstaller kurulur:

```bash
python -m pip install pyinstaller
```

Ardından proje ana klasöründe şu komut çalıştırılır:

```bash
pyinstaller --onefile --windowed --name uzaylidan-kacis --paths src --icon src\uzaylidan_kacis_oyunu\assets\app_icon.ico --add-data "src\uzaylidan_kacis_oyunu\assets;uzaylidan_kacis_oyunu/assets" src\uzaylidan_kacis_oyunu\main.py
```

Oluşan dosya şu konumda yer alır:

```text
dist/uzaylidan-kacis.exe
```

## Geliştirme Notları

Oyun mantığı `game_logic.py` dosyasına ayrılmıştır. Böylece tahmin, ipucu, hata, kazanma ve kaybetme işlemleri Tkinter arayüzünden bağımsız olarak test edilebilir. Arayüz işlemleri `gui.py`, skor kayıtları `scoreboard.py`, ses işlemleri ise `sound.py` içinde tutulur.

## Hazırlayanlar

- Gürel BİLGİN
- Ali AKSOY
