Berikut isi `README.md`-nya dalam satu variabel Python bernama `readme_text`, jadi kamu bisa langsung copy dan simpan ke file:

````python
readme_text = """
# 🤖 Asisten AI Pribadi Laptop  
Asisten cerdas yang hidup di laptopmu – bisa dikontrol lewat suara, teks, dan bahkan melihat layar!

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![OpenAI](https://img.shields.io/badge/Gemini%20API-enabled-yellow?logo=google)
![SpeechRecognition](https://img.shields.io/badge/Speech--to--Text-Active-brightgreen?logo=voximplant)
![Automation](https://img.shields.io/badge/Keyboard%2FMouse%20Control-Enabled-purple)
![License](https://img.shields.io/github/license/NatanNa12/AI-Asisten-Laptop)

---

## ✨ Fitur Utama
🎙️ **Kontrol Suara & Teks**  
➤ Bisa memahami perintah lewat suara (Speech-to-Text) atau ketikan.

🧠 **Otak AI Multimodal (Vision)**  
➤ Menganalisis tampilan layar (screenshot) dan mengeksekusi aksi seperti klik tombol, membaca teks, dll. Powered by Google Gemini API.

🖥️ **Kontrol Sistem Laptop**  
➤ Membuka aplikasi, website, mengetik otomatis, kontrol mouse, dll.

🧩 **Arsitektur Plugin Modular**  
➤ Tambahkan fitur baru seperti sistem skill.

🧠 **Memori Kontekstual & Lokasi App**  
➤ Mengingat history percakapan dan lokasi app untuk mempercepat akses.

📦 **Backup & Logging Otomatis**  
➤ Percakapan disimpan ke CSV dan didukung sistem backup.

---

## 🛠️ Teknologi yang Digunakan

| Komponen | Deskripsi |
|---------|-----------|
| 🐍 **Python** | Bahasa utama (versi 3.9+) |
| 🧠 **Gemini API** | Model AI multimodal dari Google |
| 🗣️ **SpeechRecognition + PyAudio** | Untuk input suara |
| 💬 **pyttsx3** | Text-to-speech lokal |
| 🖱️ **pyautogui** | Kontrol mouse dan keyboard |
| 📷 **PIL / mss** | Tangkap layar |
| 🔐 **dotenv** | Keamanan API key |
| 📦 **Custom Plugin Loader** | Untuk modul ekstensi |

---

## ⚙️ Instalasi & Setup

1. **Clone repository ini**
```bash
git clone https://github.com/NatanNa12/AI-Asisten-Laptop.git
cd AI-Asisten-Laptop
````

2. **Buat virtual environment**

```bash
python -m venv venv
# Aktifkan (Windows)
venv\\Scripts\\activate
# Aktifkan (Linux/macOS)
source venv/bin/activate
```

3. **Install semua dependencies**

```bash
pip install -r requirements.txt
```

4. **Atur API Key Gemini**

* Duplikat file `.env.example` jadi `.env`
* Isi dengan API Key milikmu dari Google AI Studio

5. **Jalankan aplikasi**

```bash
python main.py
```

---

## 🔄 Jalankan Otomatis Saat Startup (Windows)

> Untuk menjalankan AI ini saat laptop dinyalakan:

1. Buat file `start_ai.bat`:

```bat
@echo off
cd /d D:\\Path\\ke\\AI-Asisten-Laptop
call venv\\Scripts\\activate
python main.py
```

2. Buka **Task Scheduler** → *Create Task*

   * Tab **General**: Centang *Run with highest privileges*
   * Tab **Triggers**: *At startup*
   * Tab **Actions**: *Start a program* ➜ arahkan ke `start_ai.bat`

---

## 📁 Struktur Folder

```
AI-Asisten-Laptop/
├── main.py
├── plugins/
│   ├── kalkulator.py
│   └── ...
├── memory/
│   ├── history.csv
├── utils/
│   ├── vision.py
│   └── speech.py
├── .env.example
├── requirements.txt
└── README.md
```

---

## 💬 Kontribusi

Punya ide fitur baru? Bikin plugin baru? Pull request sangat terbuka! 💡
Silakan fork repo ini dan kirimkan kontribusimu.

---

## 📝 Lisensi

Proyek ini berlisensi MIT
"""

````

Kalau kamu mau simpan langsung ke `README.md`, kamu bisa pakai Python juga:

```python
with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_text)
````

Mau sekalian aku bantu buatkan `.bat` dan `.sh` file-nya juga? 😄
