import os
import pandas as pd
from config import DATA_DIR

def extract_raw_data():
    """สกัดข้อมูลดิบจากไฟล์ CSV ในโฟลเดอร์ data"""
    print("กำลังสกัดข้อมูลจากไฟล์ CSV...")
    
    tables = {
        'film': pd.read_csv(os.path.join(DATA_DIR, 'film.csv')),
        'category': pd.read_csv(os.path.join(DATA_DIR, 'category.csv')),
        'film_category': pd.read_csv(os.path.join(DATA_DIR, 'film_category.csv')),
        'customer': pd.read_csv(os.path.join(DATA_DIR, 'customer.csv')),
        'address': pd.read_csv(os.path.join(DATA_DIR, 'address.csv')),
        'city': pd.read_csv(os.path.join(DATA_DIR, 'city.csv')),
        'country': pd.read_csv(os.path.join(DATA_DIR, 'country.csv')),
        'rental': pd.read_csv(os.path.join(DATA_DIR, 'rental.csv')),
        'payment': pd.read_csv(os.path.join(DATA_DIR, 'payment.csv')),
        'store': pd.read_csv(os.path.join(DATA_DIR, 'store.csv')),
        'staff': pd.read_csv(os.path.join(DATA_DIR, 'staff.csv'))
    }
    print("สกัดข้อมูลจาก CSV เสร็จสิ้น!")
    return tables
