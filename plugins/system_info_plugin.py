# plugins/system_info_plugin.py
from datetime import datetime

def get_commands():
    """Mengembalikan daftar perintah yang bisa ditangani oleh plugin ini."""
    return ["jam berapa sekarang", "tanggal berapa hari ini"]

def handle_command(command: str):
    """Menangani perintah yang diberikan dan mengembalikan respons."""
    now = datetime.now()
    
    if "jam berapa" in command:
        return f"Sekarang jam {now.strftime('%H:%M')}."
    
    elif "tanggal berapa" in command:
        # Mengatur locale ke bahasa Indonesia untuk nama hari dan bulan
        import locale
        try:
            locale.setlocale(locale.LC_TIME, 'id_ID.UTF-8')
        except locale.Error:
            locale.setlocale(locale.LC_TIME, 'Indonesian_Indonesia.1252')
            
        return f"Hari ini tanggal {now.strftime('%A, %d %B %Y')}."
    
    return None