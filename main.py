# main.py (Versi dengan Wake Word)

import os
import queue
import threading
from dotenv import load_dotenv
from core.gemini_client import configure_gemini
from core.voice_input import start_voice_listener, listen_for_command # Import tambahan
from core.voice_output import speak
from core.database import log_message
from core.command_handler import execute_vision_command
from core.plugin_manager import load_plugins, execute_plugin_command
from core.knowledge import load_knowledge

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

def start_text_listener(command_queue):
    """Thread Produsen untuk input teks."""
    while True:
        try:
            # Menampilkan prompt input
            text_input = input("Anda (Ketik/Bicara): ")
            command_queue.put(text_input)
        except (EOFError, KeyboardInterrupt):
            command_queue.put("exit")
            break

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
        # Ini adalah fallback jika Anda ingin keluar tanpa memanggil Gemini
        elif command and "exit" in command.lower():
             goodbye_message = "Sistem dinonaktifkan."
             print(f"AI: {goodbye_message}")
             speak(goodbye_message)
             break


if __name__ == "__main__":
    load_dotenv()
    configure_gemini()
    main()