# core/voice_output.py
import pyttsx3

engine = None  # Mulai dengan engine diset ke None

try:
    # Menambahkan log untuk melacak proses inisialisasi
    print("⚙️  Menginisialisasi mesin Text-to-Speech (TTS)...")
    
    # Coba inisialisasi engine. Untuk Windows, driver 'sapi5' adalah default & paling stabil.
    engine = pyttsx3.init('sapi5') 
    
    # Atur beberapa properti untuk stabilitas
    engine.setProperty('rate', 170) # Kecepatan bicara (words per minute)
    
    # Cek apakah ada suara yang tersedia di sistem Anda
    voices = engine.getProperty('voices')
    if not voices:
        # Jika tidak ada voice pack terinstall, akan muncul error
        raise RuntimeError("Tidak ada paket suara (voices) TTS yang ditemukan di sistem Anda.")
    
    print("✅ Mesin TTS berhasil diinisialisasi.")

except Exception as e:
    # Jika terjadi error apapun saat inisialisasi, program tidak akan macet.
    # Asisten akan lanjut berjalan dalam mode teks saja.
    print(f"❌ PERINGATAN: Gagal menginisialisasi engine TTS. Asisten akan berjalan tanpa suara.")
    print(f"   Detail Error: {e}")
    engine = None

def speak(text: str):
    """
    Mengubah teks yang diberikan menjadi suara menggunakan engine yang sudah ada.
    """
    # Jika engine None (karena gagal diinisialisasi), fungsi ini tidak akan melakukan apa-apa.
    if not engine:
        return

    try:
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"❌ Error saat memutar suara: {e}")