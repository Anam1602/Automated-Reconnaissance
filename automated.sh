#!/bin/bash

# Banner Welcome
echo -e "\033[1;32m"
echo " _______                 ____  ___      .__         .__  __   "
echo " \\      \\ _____    _____ \\   \\/  /_____ |  |   ____ |__|/  |_ "
echo " /   |   \\\\__  \\  /     \\ \\     /\\____ \\|  |  /  _ \\|  \\   __\\"
echo "/    |    \\/ __ \\|  Y Y  \\/     \\|  |_> >  |_(  <_> )  ||  |  "
echo "\\____|__  (____  /__|_|  /___/\\  \\   __/|____/\\____/|__||__|  "
echo "        \\/     \\/      \\/      \\_/__|                         "
echo -e "\033[0m"
echo "                Welcome to NamXploit!                "
echo "              Automated Reconnaissance                "
echo

# Informasi Sosial Media
echo -e "\033[1;31mGitHub : Anam1602\033[0m"
echo -e "\033[1;31mLinkedIn : Khoirul Anam\033[0m"
echo

# Fungsi untuk memeriksa dan menginstal alat jika belum terinstal
install_if_missing() {
    if ! command -v "$1" >/dev/null 2>&1; then
        echo "Tool $1 tidak terinstal. Menginstal..."
        case "$1" in
            subfinder)
                go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
                ;;
            httpx)
                go install -v github.com/projectdiscovery/httpx/cmd/httpx@latest
                ;;
            amass)
                sudo apt install amass -y
                ;;
            katana)
                go install -v github.com/shenwei356/katana@latest
                ;;
            nuclei)
                go install -v github.com/projectdiscovery/nuclei/v2/cmd/nuclei@latest
                ;;
            assetfinder)
                go install -v github.com/tomnomnom/assetfinder@latest
                ;;
            waybackurls)
                go install -v github.com/tomnomnom/waybackurls@latest
                ;;
            gau)
                go install -v github.com/lc/gau@latest
                ;;
            subjack)
                go install -v github.com/haccer/subjack@latest
                ;;
            nikto)
                sudo apt install nikto -y
                ;;
            httprobe)
                go install -v github.com/tomnomnom/httprobe@latest
                ;;
            parallel)
                sudo apt install parallel -y
                ;;
            *)
                echo "Tidak ada instruksi instalasi untuk $1. Silakan instal secara manual."
                exit 1
                ;;
        esac
    fi
}

# Memeriksa dan menginstal alat yang diperlukan
install_if_missing "subfinder"
install_if_missing "httpx"
install_if_missing "amass"
install_if_missing "katana"
install_if_missing "nuclei"
install_if_missing "assetfinder"
install_if_missing "waybackurls"
install_if_missing "gau"
install_if_missing "subjack"
install_if_missing "nikto"
install_if_missing "httprobe"
install_if_missing "parallel"

# Meminta input domain dari pengguna
read -p "Masukkan domain (contoh: example.com): " DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "Domain tidak boleh kosong. Skrip dihentikan."
    exit 1
fi

# Menghilangkan ekstensi domain untuk nama folder
FOLDER_NAME=$(echo "$DOMAIN" | sed 's/\.[^.]*$//')

# Buat direktori untuk output
OUTPUT_DIR="/home/namxploit/Tools/bugbounty/$FOLDER_NAME"
mkdir -p "$OUTPUT_DIR"

# Daftar User-Agent untuk rotasi
USER_AGENTS=(
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15"
    "Mozilla/5.0 (Linux; Android 10; SM-A505FN) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.120 Mobile Safari/537.36"
)

# Fungsi untuk mendapatkan User-Agent secara acak
get_random_user_agent() {
    echo "${USER_AGENTS[$RANDOM % ${#USER_AGENTS[@]}]}"
}

# Subdomain enumeration menggunakan subfinder
echo "[*] Menemukan subdomain untuk $DOMAIN..."
subfinder -d "$DOMAIN" -all -o "$OUTPUT_DIR/subdomains.txt" -silent

# Subdomain enumeration menggunakan amass
echo "[*] Menemukan subdomain dengan amass..."
amass enum -d "$DOMAIN" -active -o "$OUTPUT_DIR/amass_subdomains.txt" -max-dns-queries 1000

# Gabungkan subdomain dari kedua output
cat "$OUTPUT_DIR/subdomains.txt" "$OUTPUT_DIR/amass_subdomains.txt" | sort -u > "$OUTPUT_DIR/all_subdomains.txt"

# Memeriksa status subdomain menggunakan httpx dengan jeda waktu
echo "[*] Memeriksa status subdomain menggunakan httpx..."
while read -r subdomain; do
    httpx -u "$subdomain" -status-code -o "$OUTPUT_DIR/live_subdomains.txt" -H "User-Agent: $(get_random_user_agent)"
    sleep $((RANDOM % 5 + 1))  # Jeda waktu acak antara 1-5 detik
done < "$OUTPUT_DIR/all_subdomains.txt"

# Menggunakan katana untuk memindai URL yang hidup
echo "[*] Mengumpulkan informasi tambahan dengan katana..."
katana -list "$OUTPUT_DIR/live_subdomains.txt" -o "$OUTPUT_DIR/katana_output.txt" --timeout 10 

# Menjalankan nuclei pada subdomain yang hidup dengan jeda waktu
echo "[*] Menjalankan nuclei pada subdomain yang hidup..."
while read -r subdomain; do
    nuclei -u "$subdomain" -o "$OUTPUT_DIR/nuclei_output.txt" -t "$HOME/nuclei-templates" -H "User-Agent: $(get_random_user_agent)"
    sleep $((RANDOM % 5 + 1))  # Jeda waktu acak antara 1-5 detik
done < "$OUTPUT_DIR/live_subdomains.txt"

# Menjalankan dirsearch untuk pemindaian direktori
echo "[*] Menjalankan dirsearch untuk pemindaian direktori..."
python3 /home/namxploit/dirsearch/dirsearch.py -u "http://$DOMAIN" -o "$OUTPUT_DIR/dirsearch_output.txt" -t 50 -H "User-Agent: $(get_random_user_agent)"

# Filter output dari dirsearch untuk hasil 200 dan 403
echo "[*] Menyaring hasil dari dirsearch untuk status 200 dan 403..."
grep -E "200|403" "$OUTPUT_DIR/dirsearch_output.txt" > "$OUTPUT_DIR/dirsearch_filtered.txt"

echo "[*] Proses selesai! Lihat output di direktori $OUTPUT_DIR."
