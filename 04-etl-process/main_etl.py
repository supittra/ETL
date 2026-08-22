import sys
import os
import pandas as pd
from sqlalchemy import create_engine

# 1. Setup Path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(CURRENT_DIR)

DATA_DIR = os.path.join(BASE_DIR, "data")
TARGET_DIR = os.path.join(BASE_DIR, "05-data-warehouse")
os.makedirs(TARGET_DIR, exist_ok=True)

TARGET_DB_PATH = os.path.join(TARGET_DIR, "sakila_dw.db")
TARGET_URI = f"sqlite:///{TARGET_DB_PATH}"

print("=== เริ่มต้นกระบวนการ ETL ===")

# 2. Extract
print("กำลังสกัดข้อมูลจากไฟล์ CSV...")
cust = pd.read_csv(os.path.join(DATA_DIR, 'customer.csv')).drop(columns=['last_update'], errors='ignore')
addr = pd.read_csv(os.path.join(DATA_DIR, 'address.csv')).drop(columns=['last_update'], errors='ignore')
city = pd.read_csv(os.path.join(DATA_DIR, 'city.csv')).drop(columns=['last_update'], errors='ignore')
ctry = pd.read_csv(os.path.join(DATA_DIR, 'country.csv')).drop(columns=['last_update'], errors='ignore')

film = pd.read_csv(os.path.join(DATA_DIR, 'film.csv')).drop(columns=['last_update'], errors='ignore')
film_cat = pd.read_csv(os.path.join(DATA_DIR, 'film_category.csv')).drop(columns=['last_update'], errors='ignore')
cat = pd.read_csv(os.path.join(DATA_DIR, 'category.csv')).drop(columns=['last_update'], errors='ignore')

rental = pd.read_csv(os.path.join(DATA_DIR, 'rental.csv')).drop(columns=['last_update'], errors='ignore')
payment = pd.read_csv(os.path.join(DATA_DIR, 'payment.csv')).drop(columns=['last_update'], errors='ignore')
print("สกัดข้อมูลจาก CSV เสร็จสิ้น!")

# 3. Transform
print("กำลังเข้าสู่กระบวนการ Transform...")

# Dim_Customer
dim_customer = cust.merge(addr, on='address_id') \
                   .merge(city, on='city_id') \
                   .merge(ctry, on='country_id')
dim_customer = dim_customer[['customer_id', 'first_name', 'last_name', 'email', 'active', 'city', 'country']]
dim_customer['customer_key'] = range(1, len(dim_customer) + 1)

# Dim_Film
film_cat_all = film_cat.merge(cat, on='category_id')
dim_film = film.merge(film_cat_all, on='film_id', how='left')
dim_film = dim_film[['film_id', 'title', 'release_year', 'rental_duration', 'rental_rate', 'length', 'rating', 'name']]
dim_film.rename(columns={'name': 'category_name'}, inplace=True)
dim_film['film_key'] = range(1, len(dim_film) + 1)

# Dim_Date
payment['payment_date'] = pd.to_datetime(payment['payment_date'])
unique_dates = pd.Series(payment['payment_date'].dt.date.unique())
dim_date = pd.DataFrame({'full_date': unique_dates})
dim_date['full_date'] = pd.to_datetime(dim_date['full_date'])
dim_date['date_key'] = dim_date['full_date'].dt.strftime('%Y%m%d').astype(int)
dim_date['year'] = dim_date['full_date'].dt.year
dim_date['quarter'] = dim_date['full_date'].dt.quarter
dim_date['month'] = dim_date['full_date'].dt.month
dim_date['day'] = dim_date['full_date'].dt.day
dim_date['day_of_week'] = dim_date['full_date'].dt.day_name()

# Fact_Sales
fact_sales = payment.merge(rental, on='rental_id', suffixes=('_pay', '_rent'))
fact_sales['date_key'] = pd.to_datetime(fact_sales['payment_date']).dt.strftime('%Y%m%d').astype(int)
fact_sales = fact_sales.merge(dim_customer[['customer_id', 'customer_key']], on='customer_id')
fact_sales['rental_count'] = 1
fact_sales.rename(columns={'amount': 'rental_amount'}, inplace=True)
fact_sales = fact_sales[['payment_id', 'date_key', 'customer_key', 'staff_id', 'rental_amount', 'rental_count']]

print("Transform ข้อมูลเสร็จสิ้น!")

# 4. Load
print("กำลังโหลดข้อมูลเข้าสู่ Data Warehouse...")
engine = create_engine(TARGET_URI)

dw_tables = {
    'Dim_Customer': dim_customer,
    'Dim_Film': dim_film,
    'Dim_Date': dim_date,
    'Fact_Sales': fact_sales
}

for table_name, df in dw_tables.items():
    df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
    print(f" - โหลดตาราง {table_name} สำเร็จ ({len(df)} แถว)")

print("=== สิ้นสุดการทำงานกระบวนการ ETL เสร็จสมบูรณ์! ===")
