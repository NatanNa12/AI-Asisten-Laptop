# Asisten AI Pribadi dengan Python & Gemini

Ini adalah proyek asisten AI pribadi yang dapat dikontrol melalui suara dan teks, dibangun dengan Python dan ditenagai oleh Google Gemini API. Asisten ini mampu melakukan berbagai tugas, mulai dari menjawab pertanyaan umum hingga mengontrol aplikasi di laptop Anda.

## Fitur Utama
-   **Interaksi Ganda:** Menerima perintah melalui suara (Speech-to-Text) dan ketikan keyboard.
-   **Kontrol Laptop:** Mampu membuka aplikasi, website, dan mengetik secara otomatis.
-   **Otak AI Berbasis Visi:** Menggunakan model multi-modal Gemini untuk menganalisis screenshot layar dan melakukan aksi yang relevan (misalnya, mengklik tombol).
-   **Memori & Pembelajaran:**
    -   Mengingat lokasi aplikasi yang pernah dibuka untuk akses lebih cepat di masa depan.
    -   Mengingat riwayat percakapan untuk memberikan respons yang lebih kontekstual.
-   **Sistem Plugin:** Arsitektur modular yang memungkinkan penambahan fitur baru dengan mudah.
-   **Logging & Backup:** Semua percakapan dicatat dalam file CSV dan memiliki skrip untuk backup.

## Setup & Instalasi
1.  **Clone repository ini:**
    ```bash
    git clone [https://github.com/NatanNa12/AI-Asisten-Laptop](https://github.com/NatanNa12/AI-Asisten-Laptop)
    cd NAMA_REPO_ANDA
    ```
2.  **Buat dan aktifkan virtual environment:**
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```
3.  **Install semua library yang dibutuhkan:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Konfigurasi API Key:**
    - Salin file `.env.example` menjadi file baru bernama `.env`.
    - Buka file `.env` dan masukkan API Key Gemini Anda yang valid.

5.  **Jalankan program:**
    ```bash
    python main.py
    ```