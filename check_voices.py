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