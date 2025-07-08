# core/voice_input.py
import speech_recognition as sr
# Kita tidak lagi butuh 'speak' di sini untuk menghindari circular import
# Jika diperlukan, bisa diimpor di dalam fungsi saja.

def listen_for_command() -> str | None:
    """Mendengarkan satu kali input dari mikrofon dan mengembalikannya."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # print("\n🎤 Mendengarkan untuk perintah suara...") # <-- HAPUS ATAU KOMENTARI BARIS INI
        recognizer.adjust_for_ambient_noise(source, duration=0.5) # Durasi kita kembalikan agar lebih responsif
        recognizer.pause_threshold = 1
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            # Hanya print saat suara mulai diproses, bukan saat mendengarkan
            print("\n⚙️  Mengenali suara...") 
            command = recognizer.recognize_google(audio, language='id-ID')
            print(f"✅ Suara dikenali: {command}")
            return command.lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            print("🔌 Masalah koneksi untuk pengenalan suara.")
            return None
        except Exception:
            return None

# Fungsi start_voice_listener tetap sama persis
def start_voice_listener(command_queue):
    """
    Fungsi yang akan berjalan di thread terpisah.
    Terus menerus mendengarkan dan memasukkan perintah ke dalam queue.
    """
    while True:
        command = listen_for_command()
        if command:
            command_queue.put(command)