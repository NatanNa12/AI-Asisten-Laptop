import win32com.client

try:
    speaker = win32com.client.Dispatch("SAPI.SpVOice")
    VOICE = speaker.GetVoices()
    print("Suara yang tersedia di sistem Anda:")
    for i, voice in enumerate(voices):
        print(f"{i+1}. Nama: {voice.GetDescription()}, ID: {voice.Id}")
except Exception as e:
    print(f"Gagal mendapatkan daftar suara: {e}")
    