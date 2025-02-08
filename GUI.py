# GUI ของระบบโดยใช้ Streamlit 

import streamlit as st
import requests

# URL ของ Flask API ที่คุณสร้าง
flask_api_url = "http://127.0.0.1:5000"

# หน้าเว็บ
st.title("ระบบตรวจสอบสถานะผู้ขับขี่")

# ตัวเลือกการค้นหาผู้ขับขี่
search_option = st.radio("เลือกการค้นหา:", ("ดูข้อมูลผู้ขับขี่ทั้งหมด", "ค้นหาผู้ขับขี่โดยหมายเลขใบขับขี่"))

# ฟังก์ชันนับจำนวนผู้ขับขี่แต่ละประเภท
def count_driver_types(drivers):
    type_counts = {
        'บุคคลทั่วไป': 0,
        'มือใหม่': 0,
        'คนขับรถสาธารณะ': 0
    }
    for driver in drivers:
        if driver['type'] == 'บุคคลทั่วไป':
            type_counts['บุคคลทั่วไป'] += 1
        elif driver['type'] == 'มือใหม่':
            type_counts['มือใหม่'] += 1
        elif driver['type'] == 'คนขับรถสาธารณะ':
            type_counts['คนขับรถสาธารณะ'] += 1
    return type_counts

if search_option == "ดูข้อมูลผู้ขับขี่ทั้งหมด":
    # ดึงข้อมูลจาก API
    response = requests.get(f"{flask_api_url}/drivers")
    
    if response.status_code == 200:
        data = response.json()
        st.write(data)
        
        # นับจำนวนผู้ขับขี่แต่ละประเภท
        type_counts = count_driver_types(data)
        st.subheader("จำนวนผู้ขับขี่แต่ละประเภท")
        st.write(f"บุคคลทั่วไป: {type_counts['บุคคลทั่วไป']}")
        st.write(f"มือใหม่: {type_counts['มือใหม่']}")
        st.write(f"คนขับรถสาธารณะ: {type_counts['คนขับรถสาธารณะ']}")
    else:
        st.error("ไม่สามารถดึงข้อมูลจาก API ได้")

elif search_option == "ค้นหาผู้ขับขี่โดยหมายเลขใบขับขี่":
    license_id = st.text_input("กรอกหมายเลขใบขับขี่:")
    
    if license_id:
        # ดึงข้อมูลจาก API ตามหมายเลขใบขับขี่
        response = requests.get(f"{flask_api_url}/drivers/{license_id}")
        
        if response.status_code == 200:
            data = response.json()
            st.write(data)
        else:
            st.error("ไม่พบข้อมูลผู้ขับขี่ที่คุณค้นหา")
