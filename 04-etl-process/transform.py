import pandas as pd

def transform_data(raw_data):
    """ทำความสะอาดข้อมูล รวมตาราง และคำนวณ Measures สำหรับ Data Warehouse"""
    print("กำลังเข้าสู่กระบวนการ Transform...")

    # ดึง Dataframe ออกมาและลบคอลัมน์ last_update ที่ซ้ำซ้อนออกก่อน Merge
    cust = raw_data['customer'].drop(columns=['last_update'], errors='ignore')
    addr = raw_data['address'].drop(columns=['last_update'], errors='ignore')
    city = raw_data['city'].drop(columns=['last_update'], errors='ignore')
    ctry = raw_data['country'].drop(columns=['last_update'], errors='ignore')

    # 1. Dim_Customer
    dim_customer = cust.merge(addr, on='address_id') \
                       .merge(city, on='city_id') \
                       .merge(ctry, on='country_id')
    
    dim_customer = dim_customer[['customer_id', 'first_name', 'last_name', 'email', 
                                 'active', 'city', 'country']]
    dim_customer['customer_key'] = range(1, len(dim_customer) + 1)

    # 2. Dim_Film
    film = raw_data['film'].drop(columns=['last_update'], errors='ignore')
    film_cat = raw_data['film_category'].drop(columns=['last_update'], errors='ignore')
    cat = raw_data['category'].drop(columns=['last_update'], errors='ignore')

    film_cat_all = film_cat.merge(cat, on='category_id')
    dim_film = film.merge(film_cat_all, on='film_id', how='left')
    dim_film = dim_film[['film_id', 'title', 'release_year', 'rental_duration', 
                         'rental_rate', 'length', 'rating', 'name']]
    dim_film.rename(columns={'name': 'category_name'}, inplace=True)
    dim_film['film_key'] = range(1, len(dim_film) + 1)

    # 3. Dim_Date
    payments = raw_data['payment'].copy()
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
    rental = raw_data['rental'].drop(columns=['last_update'], errors='ignore')
    fact_sales = payments.merge(rental, on='rental_id', suffixes=('_pay', '_rent'))
    fact_sales['date_key'] = pd.to_datetime(fact_sales['payment_date']).dt.strftime('%Y%m%d').astype(int)
    
    fact_sales = fact_sales.merge(dim_customer[['customer_id', 'customer_key']], on='customer_id')
    fact_sales['rental_count'] = 1
    fact_sales.rename(columns={'amount': 'rental_amount'}, inplace=True)
    
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
