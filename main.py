# main.py
import os
import queue
import threading
from dotenv import load_dotenv
from core.gemini_client import configure_gemini
from core.voice_input import start_voice_listener
from core.voice_output import speak
from core.database import log_message
from core.command_handler import execute_vision_command
from core.plugin_manager import load_plugins, execute_plugin_command
from core.knowledge import load_knowledge

# --- Kumpulan Fungsi Inti ---

def process_command(user_command):
    """Satu fungsi untuk memproses SEMUA jenis perintah."""
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
    log_message('assistant', response)

def start_text_listener(command_queue):
    """Thread Produsen untuk input teks."""
    while True:
        try:
            text_input = input()
            command_queue.put(text_input)
        except EOFError:
            # Jika input dihentikan (misal: Ctrl+Z/D), masukkan perintah keluar
            command_queue.put("exit")
            break
def main():
    """Fungsi utama yang mengatur thread dan loop konsumen."""
    load_plugins()
    load_knowledge()

# --- Fungsi Utama Program ---

def main():
    """Fungsi utama yang mengatur thread dan loop konsumen."""
    load_plugins()
    
    command_queue = queue.Queue()

    # Thread Produsen 1: Suara
    voice_thread = threading.Thread(target=start_voice_listener, args=(command_queue,), daemon=True)
    voice_thread.start()
    
    # Thread Produsen 2: Teks
    text_thread = threading.Thread(target=start_text_listener, args=(command_queue,), daemon=True)
    text_thread.start()
    
    initial_greeting = "Sistem online. Silakan bicara atau ketik perintah Anda."
    print(f"AI: {initial_greeting}")
    speak(initial_greeting)
    print("-" * 50)
    print("Anda (Ketik/Bicara): ", end="", flush=True)

    # Loop Konsumen Utama
    while True:
        # Program akan menunggu di sini sampai ada perintah masuk ke antrean
        try:
            command = command_queue.get()
            
            # Cek perintah keluar
            if command and ("exit" in command or "quit" in command or "keluar" in command):
                goodbye_message = "Sistem dinonaktifkan. Sampai jumpa lagi!"
                print(f"\nAI: {goodbye_message}")
                speak(goodbye_message)
                log_message('user', command)
                log_message('assistant', goodbye_message)
                break # Keluar dari loop utama
            
            if command:
                process_command(command)
            
            # Cetak ulang prompt setelah perintah selesai
            print("\nAnda (Ketik/Bicara): ", end="", flush=True)

        except KeyboardInterrupt:
            # Handle Ctrl+C untuk keluar
            print("\nKeluar dari program...")
            break

if __name__ == "__main__":
    load_dotenv()
    configure_gemini()
    main()