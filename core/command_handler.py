# core/command_handler.py
import os
import subprocess
import webbrowser
import pyautogui
import time
import json # Pastikan import ini ada
from .knowledge import get_app_path, set_app_path # Menggunakan . untuk relative import
from .database import load_recent_history # Menggunakan . untuk relative import
from .gemini_client import get_vision_response # Menggunakan . untuk relative import



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
    Otak utama AI. Menerjemahkan perintah bahasa natural menjadi skrip aksi bot.
    """
    try:
        screenshot = pyautogui.screenshot()
        conversation_history = load_recent_history(limit=5)

        # --- PROMPT NLU YANG SANGAT DETAIL ---
        system_prompt = """
        Anda adalah Master AI Automation yang menerjemahkan bahasa manusia menjadi daftar perintah pyautogui yang presisi.
        
        PERATURAN UTAMA:
        1.  Analisis perintah pengguna dan gambar layar untuk memahami niat dan konteks.
        2.  Uraikan perintah tersebut menjadi serangkaian aksi mouse dan keyboard yang logis.
        3.  Respons HANYA dengan sebuah list Python dalam format string JSON. Setiap item dalam list adalah sebuah string aksi.
        
        FORMAT AKSI YANG TERSEDIA:
        - "OPEN_APP(nama_aplikasi)" // Untuk membuka spotify, chrome, notepad, dll.
        - "CLICK(x, y)" // Untuk mengklik mouse.
        - "TYPE(teks)" // Untuk mengetik teks.
        - "KEY_DOWN(tombol)"  // Untuk menahan tombol (contoh: 'shift').
        - "KEY_UP(tombol)"    // Untuk melepas tombol.
        - "PRESS(tombol)"     // Untuk menekan cepat (contoh: 'enter', 'f5').
        - "SLEEP(detik)"      // Untuk jeda, penting setelah klik atau buka app.
        - "SCROLL(jumlah, arah)" // jumlah adalah pixel, arah adalah 'up' atau 'down'.
        - "ANSWER_TEXT(jawaban)" // HANYA untuk menjawab pertanyaan atau sapaan.
        
        CONTOH TERJEMAHAN:
        - Perintah: "cari milhiya di youtube" -> (Melihat layar ada Youtube) -> Respons: ["CLICK(x, y_search_bar)", "TYPE(milhiya)", "PRESS(enter)"]
        - Perintah: "tekan library di spotify" -> (Melihat layar ada Spotify) -> Respons: ["CLICK(x, y_tombol_library)"]
        - Perintah: "cari dan putar lagu 5:20 am" -> Respons: ["OPEN_APP(spotify)", "SLEEP(3)", "CLICK(x, y_search_spotify)", "TYPE(5:20 am)", "SLEEP(1)", "PRESS(enter)", "SLEEP(2)", "CLICK(x, y_hasil_pertama)"]
        
        RIWAYAT PERCAKAPAN:
        {conversation_history}
        ---
        Perintah Pengguna Saat Ini: '{command}'
        ---
        Sekarang, berikan daftar aksi dalam format string JSON:
        """
        
        print("⚙️ Menerjemahkan perintah menjadi skrip aksi...")
        full_prompt = system_prompt.format(conversation_history=conversation_history, command=command)
        response_text = get_vision_response([full_prompt, screenshot])
        print(f"🤖 Skrip aksi dari AI: {response_text}")
        
        cleaned_response = response_text.strip().replace('`', '')
        if cleaned_response.startswith("json"):
            cleaned_response = cleaned_response[4:].strip()
            
        action_list = json.loads(cleaned_response)
        
        for action_str in action_list:
            print(f"   -> Mengeksekusi: {action_str}")
            # ... (Sisa kode parsing dan eksekusi pyautogui di sini sama persis dengan sebelumnya) ...
            if action_str.startswith("CLICK"):
                params = action_str[action_str.find("(")+1:action_str.find(")")].split(',')
                pyautogui.click(int(params[0]), int(params[1]))
            elif action_str.startswith("DOUBLE_CLICK"):
                params = action_str[action_str.find("(")+1:action_str.find(")")].split(',')
                pyautogui.doubleClick(int(params[0]), int(params[1]))
            elif action_str.startswith("TYPE"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                pyautogui.write(param, interval=0.05)
            elif action_str.startswith("KEY_DOWN"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                pyautogui.keyDown(param)
            elif action_str.startswith("KEY_UP"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                pyautogui.keyUp(param)
            elif action_str.startswith("PRESS"):
                param = action_str[action_str.find("(")+1:action_str.find(")")].replace("'", "").strip()
                pyautogui.press(param.split('+'))
            elif action_str.startswith("SLEEP"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                time.sleep(float(param))
            elif action_str.startswith("SCROLL"):
                params = action_str[action_str.find("(")+1:action_str.find(")")].split(',')
                amount = int(params[0])
                direction = params[1].strip()
                pyautogui.scroll(amount if direction == 'up' else -amount)
            elif action_str.startswith("OPEN_APP"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                find_and_open_app(param) # find_and_open_app masih kita butuhkan
            elif action_str.startswith("ANSWER_TEXT"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                return param

        return "Skrip aksi telah selesai dieksekusi."

    except Exception as e:
        return f"Terjadi error dalam eksekusi skrip: {e}"