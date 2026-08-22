import sys
import os

# เพิ่ม Path ของโฟลเดอร์ 04-etl-process เพื่อให้รันข้ามโฟลเดอร์ได้ไม่มีปัญหา
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from extract import extract_raw_data
from transform import transform_data
from load import load_to_dw

if __name__ == "__main__":
    print("=== เริ่มต้นกระบวนการ ETL ===")
    
    # Step 1: Extract
    raw_data = extract_raw_data()
    
    # Step 2: Transform
    dw_data = transform_data(raw_data)
    
    # Step 3: Load
    load_to_dw(dw_data)
    
    print("=== สิ้นสุดการทำงาน ===")
