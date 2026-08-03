# TPIC İhale Monitor (GitHub Actions)

Bu proje, TPIC (Turkish Petroleum International Company) ihale sayfasını periyodik olarak kontrol eden, belirlediğiniz anahtar kelimelere uyan yeni bir ihale çıktığında bunu Telegram üzerinden size bildiren **ücretsiz** bir takip aracıdır.

Sistem, sunucu maliyeti olmadan **GitHub Actions** üzerinde 7/24 çalışacak şekilde tasarlanmıştır.

## Nasıl Kurulur?

### Adım 1: Telegram Botu Oluşturma
1. Telegram'da **@BotFather**'ı bulun ve `/newbot` komutuyla yeni bir bot oluşturun.
2. Size verilen **Bot Token**'ı kopyalayın (Örn: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`).
3. Botunuzu bulun ve `/start` diyerek bir mesaj gönderin (böylece sizinle konuşmaya başlayabilir).

### Adım 2: Chat ID Bulma
1. Telegram'da **@userinfobot** veya benzeri bir bota `/start` yazarak kendi **Chat ID**'nizi öğrenin (Örn: `987654321`).

### Adım 3: Repoyu GitHub'a Yükleme
1. Bu klasörü kendi GitHub hesabınıza yeni bir **Private (Gizli)** repository olarak yükleyin.

### Adım 4: Secrets (Gizli Anahtarlar) Ayarları
Güvenliğiniz için Telegram token ve chat id'nizi kodun içine yazmadık. GitHub reponuza eklemeniz gerekiyor:
1. GitHub reponuzda **Settings (Ayarlar)** sekmesine gidin.
2. Sol menüden **Secrets and variables > Actions** yolunu izleyin.
3. **New repository secret** butonuna tıklayın.
4. İlk Secret için:
   - Name: `TELEGRAM_BOT_TOKEN`
   - Secret: *BotFather'dan aldığınız token*
5. İkinci Secret için:
   - Name: `TELEGRAM_CHAT_ID`
   - Secret: *Kendi chat ID'niz*

### Adım 5: Sistemi Başlatma
1. Üst menüden **Actions** sekmesine tıklayın.
2. Sol menüden **TPIC Crawler**'ı seçin.
3. Sağ taraftaki **Run workflow** butonuna tıklayarak ilk taramayı manuel başlatın.
4. Bundan sonra sistem otomatik olarak **her 15 dakikada bir** çalışacaktır!

## Anahtar Kelimeleri Değiştirme
Aramak istediğiniz kelimeleri değiştirmek için `.github/workflows/crawler.yml` dosyasındaki şu satırı bulup güncelleyebilirsiniz:
```yaml
KEYWORDS: "boru, pompa, vinç, kamyon, kiralama, hidrolik, jeneratör"
```
# Crawler
