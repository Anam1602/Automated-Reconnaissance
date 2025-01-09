# Automated-Reconnaissance
Automated Reconnaissance Tool for Bug Bounty and Penetration Testing.

**Automated Reconnaissance** adalah sebuah automated reconnaissance tool yang dirancang untuk membantu bug bounty hunters dan penetration testers dalam melakukan enumerasi subdomain, pemindaian kerentanan, dan pengumpulan informasi secara otomatis. Tools ini mengintegrasikan berbagai tools populer seperti `nuclei`, `gau`, `paramspider`, `httpx`, dan lainnya.Tools ini juga di integrasikan dengan Bot Telegram agar bisa mengirim report ke bot telegram masing-masing.

---

## Fitur Utama
- **Subdomain Enumeration**: Menggunakan `nuclei`, `gau`, `paramspider`, dan `waybackurls` untuk menemukan subdomain.
- **Vulnerability Scanning**: Menggunakan `nuclei` untuk memindai kerentanan seperti SQL Injection, XSS, SSRF, dll.
- **Information Gathering**: Mengumpulkan informasi dari Wayback Machine, URL, dan parameter.
- **Telegram Integration**: Mengirim notifikasi dan hasil pemindaian ke Telegram.
- **Multithreading**: Menjalankan beberapa perintah secara paralel untuk meningkatkan kecepatan.

---

## Instalasi

### Persyaratan
- Python 3.x
- Tools yang diperlukan: `nuclei`, `gau`, `paramspider`, `httpx`, `katana`, `hakrawler`.

### Langkah-langkah
1. Clone repository ini:
   ```bash
   git clone https://github.com/Anam1602/Automated-Reconnaissance.git
   cd Automated-Reconnaissance
   pip install -r requirements.txt
   python3 automated.py

2. Requirements Tools
   Instalasi Tools
   Nuclei
   ```bash
   go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
   ```
   Gau
   ```bash
   go install -v github.com/lc/gau/v2/cmd/gau@latest
   ```
   Paramspider
   ```bash
   git clone https://github.com/devanshbatham/ParamSpider
   cd ParamSpider
   pip install -r requirements.txt
   ```
   httpx
   ```bash
   go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
   ```
   Katana
   ```bash
   go install -v github.com/projectdiscovery/katana/cmd/katana@latest
   ```
   Hakrawler
   ```bash
   go install -v github.com/hakluke/hakrawler@latest
   ```
