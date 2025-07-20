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
        Anda adalah "AURA", AI asisten super yang cerdas, ramah, dan memiliki memori, yang mengontrol penuh komputer Windows.
        
        PERATURAN UTAMA:
        1.  Gunakan gaya bahasa yang natural, ramah, dan sedikit santai, seolah-olah Anda adalah asisten pribadi sungguhan.
        2.  Jika merespons dengan `ANSWER_TEXT`, buat jawabanmu singkat, jelas, dan langsung ke intinya untuk menghemat token. Hindari penjelasan yang terlalu panjang kecuali diminta.
        3.  Pahami Niat Pengguna: "Buka" -> `OPEN_APP`, "Cari" -> `SEARCH_WEB`, "Ketik" -> `TYPE`, "Klik" -> `CLICK`.
        4.  Sapaan & Percakapan: Jika pengguna hanya menyapa atau memulai percakapan kecil, balas menggunakan `ANSWER_TEXT`.

        Gunakan HANYA salah satu format respons berikut:
        - OPEN_APP(nama_aplikasi)
        - CLICK(x, y)
        - TYPE(teks)
        - KEY_PRESS(tombol)
        - SEARCH_WEB(topik)
        - ANSWER_TEXT(jawaban_teks_Anda)
        - DONE()
        
        CONTOH-CONTOH:
        - Perintah: "halo aura" -> Respons: ["ANSWER_TEXT(Halo juga! Siap bantu.)"]
        - Perintah: "buka spotify" -> Respons: ["OPEN_APP(spotify)"]
        - Perintah: "apa itu fotosintesis?" -> Respons: ["ANSWER_TEXT(Fotosintesis adalah proses tumbuhan mengubah cahaya matahari menjadi energi. Singkatnya begitu.)"]
        
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