# core/database.py
import os
import csv
from datetime import datetime

# Tentukan lokasi file log
LOG_FOLDER = 'logs'
LOG_FILE = os.path.join(LOG_FOLDER, 'conversation_history.csv')
LOG_HEADER = ['timestamp', 'role', 'message']

def setup_log_file():
    """Memastikan folder dan file log siap digunakan."""
    # Membuat folder 'logs' jika belum ada
    os.makedirs(LOG_FOLDER, exist_ok=True)
    
    # Membuat file CSV dengan header jika file tersebut belum ada
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(LOG_HEADER)

def log_message(role: str, message: str):
    """Menyimpan pesan ke dalam file CSV."""
    # Pastikan file sudah siap
    setup_log_file()
    
    # Ambil waktu saat ini
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Buka file dalam mode 'append' (a) untuk menambahkan data baru di akhir
    with open(LOG_FILE, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Tulis baris baru berisi timestamp, peran (user/assistant), dan pesan
        writer.writerow([timestamp, role, message])
        
def load_recent_history(limit: int = 10) -> str:
    """Membaca beberapa baris terakhir dari riwayat percakapan."""
    if not os.path.exists(LOG_FILE):
        return "Tidak ada riwayat percakapan."

    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            # Membaca semua baris dan mengambil beberapa yang terakhir
            all_lines = list(csv.reader(f))
            # Ambil header + 'limit' baris terakhir
            recent_lines = all_lines[0:1] + all_lines[-limit:]
            
            # Format menjadi string yang mudah dibaca
            formatted_history = []
            for row in recent_lines[1:]: # Lewati header saat memformat
                if len(row) >= 2:
                    role, message = row[1], row[2]
                    # Ganti 'assistant' menjadi 'AI' agar lebih singkat
                    role_formatted = "AI" if role == "assistant" else "User"
                    formatted_history.append(f"{role_formatted}: {message}")
            
            return "\n".join(formatted_history)
            
    except Exception:
        return "Gagal memuat riwayat percakapan."