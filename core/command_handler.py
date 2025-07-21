import os
import subprocess
import pyautogui
import time
import json
from .knowledge import get_app_path, set_app_path
from .database import load_recent_history
from .gemini_client import get_vision_response
from .voice_output import speak

def find_and_click(image_name: str) -> bool:
    """Mencari file gambar di folder assets dan mengkliknya di layar."""
    # Menambahkan ekstensi .png secara otomatis jika tidak ada
    if not image_name.endswith('.png'):
        image_name += '.png'
        
    image_path = os.path.join('assets', 'ui_elements', image_name)
    
    if not os.path.exists(image_path):
        print(f"❌ Gambar aset tidak ditemukan: {image_path}")
        return False
        
    try:
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        if location:
            pyautogui.click(location)
            return True
        else:
            print(f"⚠️ Tidak bisa menemukan '{image_name}' di layar.")
            return False
    except Exception as e:
        print(f"Error saat mencari gambar: {e}")
        return False

# Fungsi find_and_open_app tetap sama, tidak perlu diubah
def find_and_open_app(app_name: str) -> str:
    # ... (kode fungsi ini sama seperti versi final sebelumnya) ...
    app_name_lower = app_name.lower().replace("aplikasi", "").strip()
    path_from_memory = get_app_path(app_name_lower)
    if path_from_memory:
        try:
            subprocess.Popen([path_from_memory])
            return f"Baik, membuka {app_name} dari memori."
        except Exception as e:
            return f"Gagal membuka {app_name} dari memori. Error: {e}"
    print(f"🧠 Aplikasi '{app_name}' tidak ada di memori, memulai pencarian...")
    search_paths = ['C:\\Windows\\System32', os.path.join(os.environ['APPDATA'], 'Microsoft\\Windows\\Start Menu\\Programs'), os.environ.get('ALLUSERSPROFILE') + '\\Microsoft\\Windows\\Start Menu\\Programs', 'C:\\Program Files', 'C:\\Program Files (x86)']
    for path in search_paths:
        for root, dirs, files in os.walk(path):
            for file in files:
                if (app_name_lower in file.lower()) and (file.endswith('.exe') or file.endswith('.lnk')):
                    try:
                        file_path = os.path.join(root, file)
                        subprocess.Popen([file_path])
                        set_app_path(app_name_lower, file_path)
                        return f"Baik, membuka {app_name}."
                    except Exception as e:
                        return f"Menemukan {app_name}, tapi gagal membukanya. Error: {e}"
    return f"Maaf, saya tidak dapat menemukan aplikasi bernama {app_name}."


def execute_vision_command(command: str) -> str:
    """Otak utama AI. Kini dengan kemampuan mencari gambar dan mengetik yang andal."""
    try:
        screenshot = pyautogui.screenshot()
        conversation_history = load_recent_history(limit=5)

        # --- PROMPT FINAL PALING CERDAS ---
        system_prompt = """
        Anda adalah "AURA", AI asisten super yang bisa melihat dan bertindak. Misi Anda adalah menerjemahkan perintah menjadi skrip aksi yang logis.

        PERATURAN UTAMA:
        1.  **LIHAT DULU, BARU BERTINDAK**: Selalu analisis gambar layar. Jika pengguna ingin mengklik sesuatu, jangan tebak koordinat. Gunakan `FIND_AND_CLICK(nama_file_gambar)` untuk target visual (tombol, ikon). Untuk target teks (seperti judul lagu), gunakan `TYPE` untuk mencarinya terlebih dahulu.
        2.  **Ketik Itu Perintah Utama**: Jika perintahnya jelas-jelas hanya untuk mengetik (misal: "ketik halo dunia"), langsung gunakan `TYPE(halo dunia)`. Jangan gabungkan dengan aksi lain jika tidak perlu.
        3.  **Satu Tugas per Langkah**: Uraikan tugas kompleks. Contoh: "cari lagu X dan putar" menjadi `[TYPE(X), PRESS(enter), SLEEP(2), FIND_AND_CLICK(tombol_play)]`.
        4.  **Jadilah Ramah & Efisien**: Gunakan `ANSWER_TEXT` untuk menyapa atau menjawab pertanyaan singkat.

        FORMAT AKSI (WAJIB DALAM LIST JSON):
        - "FIND_AND_CLICK(nama_file_gambar_di_assets)" // Contoh: "FIND_AND_CLICK(spotify_search_icon)"
        - "TYPE(teks)"
        - "PRESS(tombol)" // Contoh: "PRESS(enter)"
        - "OPEN_APP(nama_aplikasi)"
        - "SLEEP(detik)"
        - "ANSWER_TEXT(jawaban_singkat)"

        CONTOH-CONTOH:
        - Perintah: "ketik email untuk bos" -> Respons: ["TYPE(email untuk bos)"]
        - Perintah: "putar lagu 5:20 am" -> (Melihat Spotify terbuka) -> Respons: ["FIND_AND_CLICK(spotify_search_icon)", "SLEEP(1)", "TYPE(5:20 am)", "SLEEP(1)", "PRESS(enter)", "SLEEP(2)", "FIND_AND_CLICK(spotify_play_button)"]
        
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
        
        cleaned_response = response_text.strip().replace('`', '').replace("json", "")
        action_list = json.loads(cleaned_response)
        
        for action_str in action_list:
            print(f"   -> Mengeksekusi: {action_str}")
            if action_str.startswith("FIND_AND_CLICK"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                if not find_and_click(param):
                    return f"Aksi gagal: tidak bisa menemukan '{param}' di layar."
            elif action_str.startswith("TYPE"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                pyautogui.write(param, interval=0.05)
            elif action_str.startswith("PRESS"):
                param = action_str[action_str.find("(")+1:action_str.find(")")].replace("'", "").strip()
                pyautogui.press(param.split('+'))
            elif action_str.startswith("OPEN_APP"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                speak(find_and_open_app(param))
            elif action_str.startswith("SLEEP"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                time.sleep(float(param))
            elif action_str.startswith("ANSWER_TEXT"):
                param = action_str[action_str.find("(")+1:action_str.find(")")]
                speak(param)
        
        return "Skrip aksi telah selesai dieksekusi."

    except Exception as e:
        return f"Terjadi error dalam eksekusi skrip: {e}"