# core/gemini_client.py
import os
import google.generativeai as genai
from PIL import Image # Library untuk memproses gambar

# Variabel model dipindahkan ke dalam fungsi agar bisa diubah
text_model = None
vision_model = None

def configure_gemini():
    global text_model, vision_model
    try:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY tidak ditemukan.")
        genai.configure(api_key=api_key)
        
        # Model untuk teks (chat biasa)
        text_model = genai.GenerativeModel('gemini-1.5-flash-latest')
        
        # Model untuk visi (teks + gambar)
        vision_model = genai.GenerativeModel('gemini-1.5-flash-latest')

        print("✅ Koneksi ke Google Gemini (Teks & Visi) berhasil dikonfigurasi.")
    except Exception as e:
        print(f"❌ Terjadi kesalahan saat konfigurasi Gemini: {e}")
        exit()

# Chat session untuk percakapan teks biasa
chat = None
def get_chat_session():
    global chat
    if chat is None and text_model:
        chat = text_model.start_chat(history=[])
    return chat

def get_chat_response(prompt: str) -> str:
    chat_session = get_chat_session()
    if not chat_session:
        return "Model chat belum diinisialisasi."
    try:
        response = chat_session.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Maaf, terjadi kesalahan saat menghubungi AI: {e}"

def get_vision_response(prompt_parts) -> str:
    """
    Mengirimkan prompt multi-modal (teks + gambar) ke model visi.
    """
    if not vision_model:
        return "Model visi belum diinisialisasi."
    try:
        response = vision_model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"Maaf, terjadi kesalahan pada model visi: {e}"