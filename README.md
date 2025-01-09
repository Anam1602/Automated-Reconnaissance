<div align="center">

# NamXploit

![NamXploit Logo](https://github.com/Anam1602/Automated-Reconnaissance/raw/main/namxploit.png)

</div>

---

<div align="center">

**Welcome to NamXploit!**

**Automated Reconnaissance**

</div>

---
**Automated Reconnaissance** adalah alat otomatis untuk pemindaian subdomain dan enumerasi aset. Alat ini dirancang untuk membantu bug bounty hunters dan penetration testers dalam mengidentifikasi subdomain yang rentan.

---

## Fitur

- **Subdomain Enumeration**: Menggunakan `subfinder` dan `amass` untuk menemukan subdomain.
- **Live Subdomain Check**: Memeriksa subdomain yang aktif menggunakan `httpx`.
- **Directory Scanning**: Memindai direktori dengan `dirsearch`.
- **Vulnerability Scanning**: Menjalankan `nuclei` untuk mendeteksi kerentanan.
- **Rate Limiting**: Menghindari pemblokiran IP dengan jeda waktu dan rotasi User-Agent.

---

## Persyaratan

- **Git**: Untuk mengklon repositori.
- **Go**: Untuk menginstal alat-alat seperti `subfinder`, `httpx`, dan `nuclei`.
- **Python 3**: Untuk menjalankan `dirsearch`.

---

## Instalasi

 **Clone Repositori**:
   ```bash
   git clone https://github.com/Anam1602/Automated-Reconnaissance
   cd Automated-Reconnaissance
   chmod +x namxploit.sh
   ./automated.sh
   ```
## Usage
   ```bash
   Masukkan domain (contoh: example.com): testphp.vulnweb.com
   ```
## Konfigurasi Path Secara Manual

Beberapa alat yang digunakan dalam skrip ini memerlukan path tertentu untuk diatur secara manual. Berikut adalah panduan untuk mengkonfigurasi path tersebut:

### 1. **Dirsearch**
Dirsearch digunakan untuk memindai direktori. Pastikan Anda telah mengklon repositori `dirsearch` dan mengatur path-nya di skrip.

- **Langkah 1**: Clone repositori `dirsearch`:
  ```bash
  git clone https://github.com/maurosoria/dirsearch.git ~/dirsearch
  ```
- **Langkah 2**: buka skrip automated.sh:
  ```bash
  python3 ~/dirsearch/dirsearch.py -u "http://$DOMAIN" -o "$OUTPUT_DIR/dirsearch_output.txt" -t 50 -H "User-Agent: $(get_random_user_agent)"
  ```
- **Langkah 3**:sesuaikan `~/dirsearch/dirsearch.py` dengan path lengkap ke `dirsearch.py` di sistem Anda jika berbeda.
