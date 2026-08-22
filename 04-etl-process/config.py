import os

# กำหนด Path ของฐานข้อมูลต้นทาง (SQLite) และปลายทาง (เช่น Data Warehouse หรือ SQLite DW)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCE_DB_PATH = os.path.join(BASE_DIR, "data", "sqlite-sakila.db")
TARGET_DB_PATH = os.path.join(BASE_DIR, "05-data-warehouse", "sakila_dw.db")

SOURCE_URI = f"sqlite:///{SOURCE_DB_PATH}"
TARGET_URI = f"sqlite:///{TARGET_DB_PATH}"
