# test_db.py
from dotenv import load_dotenv
import os

load_dotenv()

db_port_value = os.getenv("DB_PORT")

print(f"Nilai DB_PORT yang terbaca adalah: <{db_port_value}>")