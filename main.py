# main.py (Versi dengan Wake Word)

import os
from dotenv import load_dotenv
from core.gemini_client import configure_gemini
# PERBAIKAN: Hanya import listen_for_command, karena start_voice_listener sudah tidak digunakan
from core.voice_input import listen_for_command 
from core.voice_output import speak
from core.database import log_message
from core.command_handler import execute_vision_command
from core.plugin_manager import load_plugins, execute_plugin_command
from core.knowledge import load_knowledge
# Di dalam file main.py

import time # Tambahkan import time di bagian atas

def main():
    """Fungsi utama yang mengatur interaksi dengan wake word."""
    load_plugins()
    load_knowledge()
    
    initial_greeting = "Sistem online. Panggil 'Gemini' untuk memulai perintah suara."
    print(f"AI: {initial_greeting}")
    speak(initial_greeting)
    print("-" * 50)

    while True:
        print("Menunggu kata panggil 'Gemini'...")
        command = listen_for_command()

        if command and "gemini" in command.lower():
            speak("Ya?")
            # Beri jeda setelah 'speak' sebelum 'listen' berikutnya
            time.sleep(0.2)
            
            actual_command = listen_for_command()
            
            if actual_command:
                if "exit" in actual_command or "quit" in actual_command or "keluar" in actual_command:
                    # ... (kode exit sama seperti sebelumnya) ...
                    goodbye_message = "Sistem dinonaktifkan. Sampai jumpa lagi!"
                    print(f"AI: {goodbye_message}")
                    speak(goodbye_message)
                    log_message('user', actual_command)
                    log_message('assistant', goodbye_message)
                    break
                
                process_command(actual_command)
            else:
                speak("Maaf, saya tidak mendengar perintah Anda.")
        
        elif command and "exit" in command.lower():
             # ... (kode exit sama seperti sebelumnya) ...
             goodbye_message = "Sistem dinonaktifkan."
             print(f"AI: {goodbye_message}")
             speak(goodbye_message)
             break
        
        # Beri jeda sangat singkat di akhir loop utama untuk stabilitas
        time.sleep(0.1)

# --- Kumpulan Fungsi Inti ---

def process_command(user_command):
    """Satu fungsi untuk memproses SEMUA jenis perintah."""
    if not user_command: # Jangan proses jika perintah kosong
        return
        
    print(f"\n>> Mengeksekusi: '{user_command}'")
    log_message('user', user_command)
    
    # Prioritas 1: Plugin
    plugin_response = execute_plugin_command(user_command)
    if plugin_response:
        response = plugin_response
    else:
        # Prioritas 2: Otak Visi
        response = execute_vision_command(user_command)
    
    print(f"AI: {response}")
    speak(response)

# --- Fungsi Utama Program ---

def main():
    """Fungsi utama yang mengatur interaksi dengan wake word."""
    load_plugins()
    load_knowledge()
    
    initial_greeting = "Sistem online. Panggil 'Gemini' untuk memulai perintah suara."
    print(f"AI: {initial_greeting}")
    speak(initial_greeting)
    print("-" * 50)

    # Loop utama program
    while True:
        # Program akan fokus mendengarkan kata panggil
        print("Menunggu kata panggil 'Gemini'...")
        command = listen_for_command()

        # Jika kata panggil terdeteksi
        if command and "gemini" in command.lower():
            speak("Ya?")
            
            # Langsung dengarkan perintah yang sebenarnya
            actual_command = listen_for_command()
            
            if actual_command:
                # Cek perintah keluar
                if "exit" in actual_command or "quit" in actual_command or "keluar" in actual_command:
                    goodbye_message = "Sistem dinonaktifkan. Sampai jumpa lagi!"
                    print(f"AI: {goodbye_message}")
                    speak(goodbye_message)
                    log_message('user', actual_command)
                    log_message('assistant', goodbye_message)
                    break # Keluar dari loop utama
                
                # Proses perintah yang sebenarnya
                process_command(actual_command)
            else:
                speak("Maaf, saya tidak mendengar perintah Anda.")
        
        # Tambahkan cara untuk keluar jika program hanya "mendengarkan"
        elif command and "exit" in command.lower():
             goodbye_message = "Sistem dinonaktifkan."
             print(f"AI: {goodbye_message}")
             speak(goodbye_message)
             break


if __name__ == "__main__":
    load_dotenv()
    configure_gemini()
    main()