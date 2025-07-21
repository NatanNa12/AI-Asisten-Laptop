# core/voice_output.py (Versi Final)
import win32com.client

speaker = None
try:
    print("⚙️  Menginisialisasi komponen Windows SAPI5...")
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    
    # Mencari suara terbaik: Prioritas #1 Wanita Indonesia, #2 Wanita mana pun
    best_voice = None
    indonesian_female_voice = None
    any_female_voice = None

    for voice in speaker.GetVoices():
        # 411 adalah kode heksadesimal 0x419 untuk Bahasa Indonesia
        if voice.Language == 411 and "female" in voice.Gender.lower():
            indonesian_female_voice = voice
            break # Langsung pilih jika ketemu
        elif "female" in voice.Gender.lower():
            any_female_voice = voice # Simpan sebagai cadangan

    if indonesian_female_voice:
        best_voice = indonesian_female_voice
    elif any_female_voice:
        best_voice = any_female_voice
    
    if best_voice:
        speaker.Voice = best_voice
        print(f"✅ Suara diatur ke: {best_voice.GetDescription()}")
    else:
        print("⚠️ Tidak ditemukan suara wanita, menggunakan suara default.")

except Exception as e:
    print(f"❌ PERINGATAN: Gagal menginisialisasi komponen SAPI5. Asisten akan berjalan tanpa suara.")
    print(f"   Detail Error: {e}")


def speak(text: str):
    if speaker:
        try:
            speaker.Speak(text)
        except Exception as e:
            print(f"❌ Error saat menggunakan SAPI5: {e}")