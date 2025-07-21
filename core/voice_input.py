# core/voice_input.py
# check_voices.py (Versi Upgrade)
import win32com.client

try:
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    voices = speaker.GetVoices()
    print("Suara yang tersedia di sistem Anda:")
    for i, voice in enumerate(voices):
        # 411 adalah kode untuk bahasa Indonesia, 409 untuk US English
        lang_id = voice.Language
        print(f"{i+1}. Nama: {voice.GetDescription()}, Language ID: {lang_id}")
except Exception as e:
    print(f"Gagal mendapatkan daftar suara: {e}")

def listen_for_command() -> str | None:
    """
    Mendengarkan satu kali input dari mikrofon dan mengembalikannya sebagai teks.
    Fungsi ini dibuat "senyap" untuk tidak mengganggu terminal.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Mengatur sensitivitas terhadap kebisingan
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        recognizer.pause_threshold = 1
        
        try:
            # Merekam audio dari mikrofon
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)
            
            # Hanya print saat suara mulai diproses
            print("⚙️  Mengenali suara...") 
            command = recognizer.recognize_google(audio, language='id-ID')
            print(f"✅ Suara dikenali: {command}")
            return command.lower()
            
        except sr.UnknownValueError:
            # Jika suara tidak jelas, kembalikan None tanpa pesan error
            return None
        except sr.RequestError:
            print("🔌 Masalah koneksi untuk pengenalan suara.")
            return None
        except Exception:
            # Untuk error lainnya
            return None