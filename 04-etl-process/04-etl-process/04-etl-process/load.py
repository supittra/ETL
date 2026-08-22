from sqlalchemy import create_engine
from config import TARGET_URI

def load_to_dw(transformed_data):
    """นำข้อมูลเข้าสู่ Data Warehouse Target Database"""
    engine = create_engine(TARGET_URI)
    print("กำลังโหลดข้อมูลเข้าสู่ Data Warehouse...")

    for table_name, df in transformed_data.items():
        # replace = ลบตารางเก่าถ้ามีอยู่แล้ว และสร้างตารางใหม่พร้อมใส่ข้อมูล
        df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)
        print(f" - โหลดตาราง {table_name} สำเร็จ ({len(df)} แถว)")

    print("กระบวนการ ETL เสร็จสมบูรณ์ทุกขั้นตอน!")
