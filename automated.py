import os
import subprocess
import requests
import re
import logging
import time
from concurrent.futures import ThreadPoolExecutor

# ASCII Art for "Automated"
automated_banner = """
    ___         __                        __           __   
   /   | __  __/ /_____  ____ ___  ____ _/ /____  ____/ /   
  / /| |/ / / / __/ __ \/ __ `__ \/ __ `/ __/ _ \/ __  /    
 / ___ / /_/ / /_/ /_/ / / / / / / /_/ / /_/  __/ /_/ /     
/_/  |_\__,_/\__/\____/_/ /_/ /_/\__,_/\__/\___/\__,_/  
"""

print(automated_banner)
print("By NamXploit\n")

# Setup logging
logging.basicConfig(filename="namxploit.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load environment variables
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7447060549:AAGMgWudQNts38MULPNZLxzGhK8aXqql3lk")  # Ganti dengan token bot Anda
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "1542475607")  # Ganti dengan chat ID Anda

# Fungsi untuk mengirim pesan ke Telegram
def send_message(bot_token, chat_id, text):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send message: {e}")

# Fungsi untuk mengirim file ke Telegram
def send_document(bot_token, chat_id, document_path):
    url = f"https://api.telegram.org/bot{bot_token}/sendDocument"
    try:
        with open(document_path, "rb") as file:
            files = {"document": file}
            data = {"chat_id": chat_id}
            response = requests.post(url, files=files, data=data)
            response.raise_for_status()
    except Exception as e:
        logging.error(f"Failed to send document: {e}")

# Fungsi untuk menjalankan perintah shell
def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            error_message = result.stderr.decode().strip()
            logging.error(f"Command failed: {command}\nError: {error_message}")
            send_message(BOT_TOKEN, CHAT_ID, f"❌ Error: {command}\n{error_message}")
            return False
        return True
    except Exception as e:
        logging.error(f"Exception in run_command: {e}")
        return False

# Fungsi untuk validasi domain
def validate_domain(domain):
    pattern = r"^([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
    return re.match(pattern, domain) is not None

# Fungsi untuk menjalankan recon
def run_recon(domain):
    commands = [
        f"echo {domain} | nuclei -silent -t ~/nuclei-templates/http/vulnerabilities/wordpress -o output/nuclei/wpscann-{domain}-nuclei.txt",
        f"echo {domain} | gau --subs --blacklist png,jpg,gif,jpeg,swf,woff,svg,pdf,css,webp,woff,woff2,eot,ttf,otf,mp4 | urldedupe -s | gf lfi redirect sqli-error sqli ssrf ssti xss xxe | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result1-{domain}.txt",
        f"echo {domain} | gau --subs --blacklist png,jpg,gif,jpeg,swf,woff,svg,pdf,css,webp,woff,woff2,eot,ttf,otf,mp4 | urldedupe -s | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result2-{domain}.txt",
        f"echo {domain} | waybackurls | urldedupe -s | gf lfi redirect sqli-error sqli ssrf ssti xss xxe | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result3-{domain}.txt",
        f"echo {domain} | waybackurls | urldedupe -s | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result4-{domain}.txt",
        f"echo {domain} | gauplus | urldedupe -s | gf lfi redirect sqli-error sqli ssrf ssti xss xxe | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result5-{domain}.txt",
        f"echo {domain} | gauplus | urldedupe -s | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result6-{domain}.txt",
        f"paramspider -d {domain} -o output/paramspider/",
        f"cat output/paramspider/results/{domain}.txt | urldedupe -s | gf lfi redirect sqli-error sqli ssrf ssti xss xxe | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result7-{domain}.txt",
        f"cat output/paramspider/results/{domain}.txt | urldedupe -s | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result8-{domain}.txt",
        f"echo {domain} | httpx -silent | katana -silent | urldedupe -s | gf lfi redirect sqli-error sqli ssrf ssti xss xxe | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result9-{domain}.txt",
        f"echo {domain} | httpx -silent | katana -silent | urldedupe -s | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result10-{domain}.txt",
        f"echo {domain} | httpx -silent | hakrawler -subs -u | urldedupe -s | gf lfi redirect sqli-error sqli ssrf ssti xss xxe | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result11-{domain}.txt",
        f"echo {domain} | httpx -silent | hakrawler -subs -u | urldedupe -s | qsreplace FUZZ | grep FUZZ | nuclei -silent -t ~/nuclei-templates/dast/vulnerabilities -dast -o output/nuclei/result12-{domain}.txt",
        f"echo {domain} | nuclei -silent -t ~/nuclei-templates/http/exposures -o output/nuclei/exposures-{domain}.txt",
        f"echo {domain} | nuclei -silent -t ~/nuclei-templates/http/exposed-panels -o output/nuclei/exposed-panels-{domain}.txt",
        f"echo {domain} | nuclei -silent -t ~/nuclei-templates/http/default-logins/ -o output/nuclei/default-logins-1-{domain}.txt",
        f"echo {domain} | nuclei -silent -t ~/nuclei-templates/default-logins -o output/nuclei/default-logins-2-{domain}.txt",
    ]

    with ThreadPoolExecutor(max_workers=5) as executor:
        for command in commands:
            executor.submit(run_command, command)
            time.sleep(2)  # Rate limiting

# Fungsi untuk menggabungkan hasil
def generate_final_result(domain):
    run_command(f"cat output/nuclei/*.txt | anew output/final/final-result-{domain}.txt")

# Fungsi untuk menghapus file sementara
def delete_temp_files(domain):
    run_command(f"rm -rf output/nuclei/*.txt output/paramspider/results/{domain}.txt")

# Main function
def main():
    domain = input("Enter the domain (without http/https): ").strip()

    if not validate_domain(domain):
        print("❌ Invalid domain format. Please enter a valid domain.")
        send_message(BOT_TOKEN, CHAT_ID, "❌ Invalid domain format. Please enter a valid domain.")
        exit(1)

    # Buat struktur direktori
    os.makedirs("output/nuclei", exist_ok=True)
    os.makedirs("output/paramspider/results", exist_ok=True)
    os.makedirs("output/final", exist_ok=True)

    send_message(BOT_TOKEN, CHAT_ID, f"🚀 Starting scan for {domain}, happy hunting...")

    run_recon(domain)
    generate_final_result(domain)

    send_message(BOT_TOKEN, CHAT_ID, f"✅ Scan for {domain} completed. Sending results...")
    send_document(BOT_TOKEN, CHAT_ID, f"output/final/final-result-{domain}.txt")

    delete_temp_files(domain)
    logging.info(f"Scan completed for domain: {domain}")

if __name__ == "__main__":
    main()
