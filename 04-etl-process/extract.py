import pandas as pd
from sqlalchemy import create_engine
from config import SOURCE_URI

def extract_raw_data():
    """สกัดข้อมูลดิบจากฐานข้อมูล OLTP ต้นทาง"""
    engine = create_engine(SOURCE_URI)
    
    print("กำลังสกัดข้อมูลจาก OLTP Source...")
    tables = {
        'film': pd.read_sql("SELECT * FROM film", engine),
        'category': pd.read_sql("SELECT * FROM category", engine),
        'film_category': pd.read_sql("SELECT * FROM film_category", engine),
        'customer': pd.read_sql("SELECT * FROM customer", engine),
        'address': pd.read_sql("SELECT * FROM address", engine),
        'city': pd.read_sql("SELECT * FROM city", engine),
        'country': pd.read_sql("SELECT * FROM country", engine),
        'rental': pd.read_sql("SELECT * FROM rental", engine),
        'payment': pd.read_sql("SELECT * FROM payment", engine),
        'store': pd.read_sql("SELECT * FROM store", engine),
        'staff': pd.read_sql("SELECT * FROM staff", engine)
    }
    print("สกัดข้อมูลเสร็จสิ้น!")
    return tables
