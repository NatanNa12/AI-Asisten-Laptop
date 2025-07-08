# core/knowledge.py
import os
import json

KNOWLEDGE_FILE = 'knowledge_base.json'
knowledge_data = {}

def load_knowledge():
    """Memuat knowledge base dari file JSON saat startup."""
    global knowledge_data
    if os.path.exists(KNOWLEDGE_FILE):
        with open(KNOWLEDGE_FILE, 'r') as f:
            knowledge_data = json.load(f)
    else:
        # Jika file tidak ada, buat struktur dasarnya
        knowledge_data = {'app_paths': {}}
        _save_knowledge()

def _save_knowledge():
    """Menyimpan data pengetahuan ke file JSON."""
    with open(KNOWLEDGE_FILE, 'w') as f:
        json.dump(knowledge_data, f, indent=4)

def get_app_path(app_name: str) -> str | None:
    """Mencari path aplikasi dari knowledge base."""
    return knowledge_data.get('app_paths', {}).get(app_name.lower())

def set_app_path(app_name: str, path: str):
    """Menyimpan path aplikasi yang baru ditemukan ke knowledge base."""
    app_name = app_name.lower()
    if 'app_paths' not in knowledge_data:
        knowledge_data['app_paths'] = {}
    knowledge_data['app_paths'][app_name] = path
    _save_knowledge()
    print(f"🧠 Pengetahuan baru disimpan: Lokasi '{app_name}' adalah '{path}'.")