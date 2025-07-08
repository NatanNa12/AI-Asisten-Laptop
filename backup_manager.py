# backup_manager.py
import os
import shutil
from datetime import datetime

# --- KONFIGURASI ---
# Lokasi file log asli yang ingin di-backup
SOURCE_FILE = os.path.join('logs', 'conversation_history.csv')

# Lokasi folder tujuan backup di Drive D:
# Anda bisa mengubah 'Assistant_Backup' sesuai keinginan.
BACKUP_FOLDER = 'D:\\Assistant_Backup'
# --------------------


def run_backup():
    """
    Menjalankan proses backup file log percakapan.
    """
    print("🚀 Memulai proses backup...")

    # 1. Cek apakah file sumber ada
    if not os.path.exists(SOURCE_FILE):
        print(f"❌ Error: File sumber tidak ditemukan di '{SOURCE_FILE}'. Tidak ada yang di-backup.")
        return

    # 2. Cek apakah folder backup ada, jika tidak, buat folder tersebut
    try:
        if not os.path.exists(BACKUP_FOLDER):
            os.makedirs(BACKUP_FOLDER)
            print(f"📁 Folder backup dibuat di '{BACKUP_FOLDER}'.")
    except OSError as e:
        print(f"❌ Gagal membuat folder backup di '{BACKUP_FOLDER}'. Error: {e}")
        return

    # 3. Buat nama file backup yang unik dengan timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file_name = f'conversation_history_{timestamp}.csv'
    destination_path = os.path.join(BACKUP_FOLDER, backup_file_name)

    # 4. Salin file sumber ke lokasi tujuan
    try:
        shutil.copy2(SOURCE_FILE, destination_path)
        print(f"✅ Backup berhasil disimpan ke:")
        print(f"   {destination_path}")
    except Exception as e:
        print(f"❌ Gagal menyalin file. Error: {e}")


if __name__ == '__main__':
    run_backup()