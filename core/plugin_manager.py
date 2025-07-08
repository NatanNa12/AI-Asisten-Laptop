# core/plugin_manager.py
import os
import importlib.util

# Dictionary untuk menyimpan peta dari perintah ke fungsi handler-nya
plugin_command_map = {}

def load_plugins():
    """Mencari dan memuat semua plugin dari folder /plugins."""
    plugins_dir = 'plugins'
    print("🔌 Memuat plugin...")
    
    # Cari semua file python di dalam folder plugins
    for filename in os.listdir(plugins_dir):
        if filename.endswith('_plugin.py'):
            plugin_name = filename[:-3]
            try:
                # Import file plugin secara dinamis
                spec = importlib.util.spec_from_file_location(plugin_name, os.path.join(plugins_dir, filename))
                plugin_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(plugin_module)
                
                # Panggil fungsi get_commands() dari plugin
                commands = plugin_module.get_commands()
                for command in commands:
                    # Daftarkan setiap perintah ke dalam map
                    plugin_command_map[command] = plugin_module.handle_command
                print(f"   -> Plugin '{plugin_name}' berhasil dimuat dengan perintah: {', '.join(commands)}")
            
            except Exception as e:
                print(f"   -> ❌ Gagal memuat plugin '{filename}'. Error: {e}")

def execute_plugin_command(user_command: str) -> str | None:
    """
    Mengeksekusi perintah plugin jika ada yang cocok.
    """
    for command_trigger in plugin_command_map:
        if command_trigger in user_command:
            # Jika pemicu ditemukan di perintah pengguna, panggil fungsi handler-nya
            handler_function = plugin_command_map[command_trigger]
            return handler_function(user_command)
    
    return None