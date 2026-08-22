import os

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

# ชี้ไปที่โฟลเดอร์ data ที่เก็บไฟล์ CSV
DATA_DIR = os.path.join(BASE_DIR, "data")

# สร้างโฟลเดอร์ 05-data-warehouse สำหรับเก็บไฟล์ปลายทาง
TARGET_DIR = os.path.join(BASE_DIR, "05-data-warehouse")
os.makedirs(TARGET_DIR, exist_ok=True)

TARGET_DB_PATH = os.path.join(TARGET_DIR, "sakila_dw.db")
TARGET_URI = f"sqlite:///{TARGET_DB_PATH}"
