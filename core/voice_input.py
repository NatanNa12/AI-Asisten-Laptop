# core/voice_output.py
import win32com.client

speaker = None
try:
    print("⚙️  Menginisialisasi komponen Windows SAPI5...")
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    
    # Mencari suara wanita yang tersedia
    found_female_voice = False
    for voice in speaker.GetVoices():
        if "zira" in voice.GetDescription().lower() or "female" in voice.GetDescription().lower():
            speaker.Voice = voice
            print(f"✅ Suara diatur ke: {voice.GetDescription()}")
            found_female_voice = True
            break
    
    if not found_female_voice:
        print("⚠️ Tidak ditemukan suara wanita spesifik, menggunakan suara default.")

except Exception as e:
    print(f"❌ PERINGATAN: Gagal menginisialisasi komponen SAPI5. Asisten akan berjalan tanpa suara.")
    print(f"   Detail Error: {e}")


def speak(text: str):
    """
    Mengubah teks menjadi suara menggunakan Windows SAPI5 COM object.
    """
    if speaker:
        try:
            speaker.Speak(text)
        except Exception as e:
            print(f"❌ Error saat menggunakan SAPI5: {e}")