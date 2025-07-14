 """# 🤖 Asisten AI Pribadi Laptop  
Asisten cerdas yang hidup di laptopmu – bisa dikontrol lewat suara, teks, dan bahkan melihat layar!

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)  
![OpenAI](https://img.shields.io/badge/Gemini%20API-enabled-yellow?logo=google)  
![SpeechRecognition](https://img.shields.io/badge/Speech--to--Text-Active-brightgreen?logo=voximplant)  
![Automation](https://img.shields.io/badge/Keyboard%2FMouse%20Control-Enabled-purple)  
![License](https://img.shields.io/github/license/NatanNa12/AI-Asisten-Laptop)

---

## ✨ Fitur Utama

### 🗣️ Kontrol Suara & Teks  
▶ Bisa memahami perintah lewat suara (Speech-to-Text) atau ketikan.

### 🧠 Otak AI Multimodal (Vision)  
▶ Menganalisis tampilan layar (screenshot) dan mengeksekusi aksi seperti klik tombol, membaca teks, dll. Powered by Gemini API.

### 🖥️ Kontrol Sistem Laptop  
▶ Membuka aplikasi, website, mengetik otomatis, kontrol mouse, dll.

### 🧩 Arsitektur Plugin Modular  
▶ Tambahkan fitur baru seperti sistem skill.

### 💾 Memori & Pembelajaran  
▶ Mengingat history percakapan dan lokasi aplikasi yang pernah dibuka.

### 📦 Logging & Backup  
▶ Semua interaksi dicatat ke CSV dan bisa dibackup otomatis.

---

## 🛠️ Teknologi yang Digunakan

| Komponen | Deskripsi |
|---------|-----------|
| 🐍 **Python** | Bahasa utama proyek |
| 🧠 **Gemini API** | AI multimodal Google |
| 🗣️ **SpeechRecognition + PyAudio** | Input suara |
| 💬 **pyttsx3** | Text-to-speech |
| 🖱️ **pyautogui** | Kontrol keyboard & mouse |
| 📷 **PIL / mss** | Screenshot layar |
| 🔐 **dotenv** | Konfigurasi API key |
| ⚙️ **Plugin Loader** | Sistem modular ekstensi |

---

## ⚙️ Cara Instalasi

```bash
# 1. Clone repo
git clone https://github.com/NatanNa12/AI-Asisten-Laptop.git
cd AI-Asisten-Laptop

# 2. Buat virtual environment
python -m venv venv

# 3. Aktifkan environment
# Windows:
venv\\Scripts\\activate
# macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Konfigurasi .env
cp .env.example .env
# lalu masukkan API_KEY dari Google Gemini

# 6. Jalankan AI
python main.py
````

---

## 🔄 Auto Startup (Windows)

1. Buat file `start_ai.bat`:

```bat
@echo off
cd /d D:\\Path\\ke\\AI-Asisten-Laptop
call venv\\Scripts\\activate
python main.py
```

2. Buka **Task Scheduler**:

   * Create Task → General: Centang “Run with highest privileges”
   * Triggers: At startup
   * Actions: Start program → arahkan ke `start_ai.bat`

---

## 📁 Struktur Folder

```
AI-Asisten-Laptop/
├── main.py
├── plugins/
│   ├── kalkulator.py
├── memory/
│   ├── history.csv
├── utils/
│   ├── vision.py
│   └── speech.py
├── .env.example
├── requirements.txt
└── README.md