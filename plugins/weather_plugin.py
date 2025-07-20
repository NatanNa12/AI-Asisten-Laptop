# plugins/weather_plugin.py
import os
import requests

def get_commands():
    return ["cuaca di"]

def handle_command(command: str):
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "API Key untuk OpenWeatherMap belum diatur di file .env."

    try:
        city = command.split("cuaca di", 1)[1].strip()
        if not city:
            return "Kota mana yang ingin Anda ketahui cuacanya?"

        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric&lang=id"
        response = requests.get(url).json()

        if response["cod"] == 200:
            desc = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            feels_like = response["main"]["feels_like"]
            return f"Cuaca di {city} saat ini {desc}, dengan suhu sekitar {temp:.0f} derajat celsius, terasa seperti {feels_like:.0f} derajat."
        else:
            return f"Maaf, saya tidak bisa menemukan data cuaca untuk {city}."
    except Exception:
        return "Maaf, terjadi kesalahan saat mengambil data cuaca."
    