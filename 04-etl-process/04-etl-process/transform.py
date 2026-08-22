import pandas as pd

def transform_data(raw_data):
    """ทำความสะอาดข้อมูล รวมตาราง และคำนวณ Measures สำหรับ Data Warehouse"""
    print("กำลังเข้าสู่กระบวนการ Transform...")

    # 1. Dim_Customer (Denormalization: Customer + Address + City + Country)
    dim_customer = raw_data['customer'].merge(raw_data['address'], on='address_id') \
                                       .merge(raw_data['city'], on='city_id') \
                                       .merge(raw_data['country'], on='country_id')
    
    dim_customer = dim_customer[['customer_id', 'first_name', 'last_name', 'email', 
                                 'active', 'city', 'country']]
    dim_customer['customer_key'] = range(1, len(dim_customer) + 1) # Surrogate Key

    # 2. Dim_Film (Film + Category)
    film_cat = raw_data['film_category'].merge(raw_data['category'], on='category_id')
    dim_film = raw_data['film'].merge(film_cat, on='film_id', how='left')
    dim_film = dim_film[['film_id', 'title', 'release_year', 'rental_duration', 
                         'rental_rate', 'length', 'rating', 'name']]
    dim_film.rename(columns={'name': 'category_name'}, inplace=True)
    dim_film['film_key'] = range(1, len(dim_film) + 1)

    # 3. Dim_Date (แตกมิติเวลาจาก Payment/Rental)
    payments = raw_data['payment']
    payments['payment_date'] = pd.to_datetime(payments['payment_date'])
    
    unique_dates = pd.Series(payments['payment_date'].dt.date.unique())
    dim_date = pd.DataFrame({'full_date': unique_dates})
    dim_date['full_date'] = pd.to_datetime(dim_date['full_date'])
    dim_date['date_key'] = dim_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['quarter'] = dim_date['full_date'].dt.quarter
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['day'] = dim_date['full_date'].dt.day
    dim_date['day_of_week'] = dim_date['full_date'].dt.day_name()

    # 4. Fact_Sales
    # Join Payment กับ Rental เพื่อหาข้อมูลการขายแบบครบถ้วน
    fact_sales = payments.merge(raw_data['rental'], on='rental_id', suffixes=('_pay', '_rent'))
    
    # แปลงวันที่เพื่อ Map กับ Date Key
    fact_sales['date_key'] = pd.to_datetime(fact_sales['payment_date']).dt.strftime('%Y%m%d').astype(int)
    
    # Map Surrogate Keys
    fact_sales = fact_sales.merge(dim_customer[['customer_id', 'customer_key']], on='customer_id')
    
    # สร้าง Measures
    fact_sales['rental_count'] = 1
    fact_sales.rename(columns={'amount': 'rental_amount'}, inplace=True)
    
    # เลือกเฉพาะคอลัมน์ที่จะเก็บใน Fact Table
    fact_sales = fact_sales[['payment_id', 'date_key', 'customer_key', 'staff_id', 
                             'rental_amount', 'rental_count']]

    transformed_data = {
        'Dim_Customer': dim_customer,
        'Dim_Film': dim_film,
        'Dim_Date': dim_date,
        'Fact_Sales': fact_sales
    }
    
    print("Transform ข้อมูลเสร็จสิ้น!")
    return transformed_data
