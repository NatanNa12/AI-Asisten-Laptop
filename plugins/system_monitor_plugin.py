import psutil

def get_command():
    return ["status sistem", "penggunaan cpu", "penggunaan ram"]

def handle_command(command: str):
    if "cpu" in command:
        cpu_usage = psutil.cpu_percent(interval=1)
        return f"penggunaan CPU saat ini adalah{cpu_usage} persen"
    elif "ram" in command:
        ram_usage = psutil.virtual_memory().percent
        return f"Penggunaan RAM saat ini adalah{ram_usage} persen"
    elif "sistem" in command:
        cpu = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory().percent
        return f"Tentu, status sistem saat ini: CPU pada {cpu} persen, dan RAM pada {ram} persen."
    return None
    