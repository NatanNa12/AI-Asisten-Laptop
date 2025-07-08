# core/command_handler.py
import os
import subprocess
import webbrowser
import pyautogui
import time
from core.gemini_client import get_vision_response
from PIL import Image

from core.knowledge import get_app_path, set_app_path # Tambahkan import ini
from core.database import load_recent_history

def find_and_open_app(app_name: str) -> str:
    """Mencari dan membuka aplikasi menggunakan knowledge base."""
    app_name_lower = app_name.lower().replace("aplikasi", "").strip()
    
    # 1. Cek memori (knowledge base) terlebih dahulu
    path_from_memory = get_app_path(app_name_lower)
    if path_from_memory:
        try:
            os.startfile(path_from_memory)
            return f"Baik, membuka {app_name} dari memori."
        except Exception as e:
            return f"Gagal membuka {app_name} dari memori. Error: {e}"
    
    # 2. Jika tidak ada di memori, baru lakukan pencarian
    print(f"🧠 Aplikasi '{app_name}' tidak ada di memori, memulai pencarian...")
    search_paths = [
        'C:\\Windows\\System32',
        os.path.join(os.environ['APPDATA'], 'Microsoft\\Windows\\Start Menu\\Programs'),
        os.environ.get('ALLUSERSPROFILE') + '\\Microsoft\\Windows\\Start Menu\\Programs',
        'C:\\Program Files',
        'C:\\Program Files (x86)',
    ]
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if (app_name_lower in file.lower()) and (file.endswith('.exe') or file.endswith('.lnk')):
                    try:
                        file_path = os.path.join(root, file)
                        os.startfile(file_path)
                        # 3. Setelah ditemukan, simpan ke memori!
                        set_app_path(app_name_lower, file_path)
                        return f"Baik, membuka {app_name}."
                    except Exception as e:
                        return f"Menemukan {app_name}, tapi gagal membukanya. Error: {e}"

    return f"Maaf, saya tidak dapat menemukan aplikasi bernama {app_name}."

def execute_vision_command(command: str) -> str:
    """
    Otak utama AI. Kini dengan memori percakapan.
    """
    try:
        screenshot = pyautogui.screenshot()
        # Ambil 10 percakapan terakhir sebagai memori
        conversation_history = load_recent_history(limit=10)

        system_prompt = """
        Anda adalah AI asisten super yang cerdas, ramah, dan memiliki memori. Anda mengontrol penuh komputer Windows.
        Misi Anda adalah memahami niat pengguna dan mengubahnya menjadi satu aksi komputer yang paling tepat.

        PERATURAN PENTING:
        1.  Gunakan "RIWAYAT PERCAKAPAN" untuk memahami konteks. Jika pengguna berkata "lanjutkan", lihat apa yang sedang dibicarakan. Jika pengguna bercerita, berikan respons yang relevan dan empatik.
        2.  Pahami Niat Pengguna: "Buka" -> `OPEN_APP`, "Cari" -> `SEARCH_WEB`, "Ketik" -> `TYPE`, "Klik" -> `CLICK`.
        3.  Sapaan & Percakapan: Jika pengguna hanya menyapa atau bercerita, balas menggunakan `ANSWER_TEXT`. Jangan melakukan aksi komputer jika tidak diminta secara eksplisit.

        Gunakan HANYA salah satu format respons berikut:
        - OPEN_APP(nama_aplikasi)
        - CLICK(x, y)
        - TYPE(teks)
        - KEY_PRESS(tombol)
        - SEARCH_WEB(topik)
        - ANSWER_TEXT(jawaban_teks_Anda)
        - DONE()

        ---
        RIWAYAT PERCAKapan TERAKHIR (untuk konteks):
        {conversation_history}
        ---

        Konteks Saat Ini:
        - Perintah Pengguna: '{command}'
        """
        
        print("⚙️  Menganalisis layar dan memori percakapan...")
        # Kirim prompt yang sudah diformat dengan riwayat dan perintah
        full_prompt = system_prompt.format(conversation_history=conversation_history, command=command)
        response_action = get_vision_response([full_prompt, screenshot])
        print(f"🤖 Aksi yang disarankan AI: {response_action}")
        
        action = response_action.strip()
        
        # (Sisa kode parsing di bawah ini tidak perlu diubah, biarkan seperti adanya)
        # ... (salin-tempel sisa fungsi dari versi sebelumnya) ...
        if action.startswith("CLICK"):
            coords_str = action[action.find("(")+1:action.find(")")].split(',')
            x, y = int(coords_str[0]), int(coords_str[1])
            pyautogui.click(x, y)
            return f"Melakukan klik di {x}, {y}."
        elif action.startswith("TYPE"):
            text_to_type = action[action.find("(")+1:action.find(")")]
            pyautogui.write(text_to_type, interval=0.05)
            return f"Mengetik: {text_to_type}."
        elif action.startswith("KEY_PRESS"):
            key = action[action.find("(")+1:action.find(")")].replace("'", "").strip()
            pyautogui.press(key.split('+'))
            return f"Menekan tombol '{key}'."
        elif action.startswith("OPEN_APP"):
            app_name = action[action.find("(")+1:action.find(")")]
            return find_and_open_app(app_name)
        elif action.startswith("SEARCH_WEB"):
            query = action[action.find("(")+1:action.find(")")]
            webbrowser.open(f'https://www.google.com/search?q={query}')
            return f"Mencari '{query}' di web."
        elif action.startswith("ANSWER_TEXT"):
            answer = action[action.find("(")+1:action.find(")")]
            return answer
        elif action.startswith("DONE"):
            return "Tugas selesai."
        else:
            return action


    except Exception as e:
        return f"Terjadi error pada mode visi: {e}"
    
    