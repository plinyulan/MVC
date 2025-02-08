# ใช้ Flask ในการทำ API เพี่อที่จะดึงข้อมูลจาก data.json

from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# อ่านข้อมูลจากไฟล์ data.json
import json
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# คำนวณอายุจากวันเกิด
def calculate_age(birthdate):
    birth_date = datetime.strptime(birthdate, "%Y-%m-%d")
    today = datetime.today()
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    return age

# ฟังก์ชันตรวจสอบสถานะของผู้ขับขี่
def check_status(driver):
    age = calculate_age(driver['birthdate'])
    
    if driver['type'] == 'บุคคลทั่วไป':
        if age > 70:
            driver['status'] = 'หมดอายุ'
        elif age < 16:
            driver['status'] = 'ถูกระงับ'
        else:
            driver['status'] = 'ปกติ'
            driver['action'] = 'ทดสอบสมรรถนะ'
    
    elif driver['type'] == 'มือใหม่':
        if age > 50:
            driver['status'] = 'หมดอายุ'
        elif age < 16:
            driver['status'] = 'ถูกระงับ'
        else:
            driver['status'] = 'ปกติ'
            driver['action1'] = 'สอบข้อเขียน'
            driver['action2'] = 'สอบปฏิบัติ'

    elif driver['type'] == 'คนขับรถสาธารณะ':
        if age > 60:
            driver['status'] = 'หมดอายุ'
        elif age < 20:
            driver['status'] = 'ถูกระงับ'
        else:
            driver['status'] = 'ปกติ'
            complaints = driver.get('complaints', 0)
            if complaints > 5:
                driver['status'] = 'ถูกระงับชั่วคราว'
                driver['action'] = 'อบรม'
            else:
                driver['action'] = 'ทดสอบสมรรถนะ'
    return driver

@app.route('/drivers', methods=['GET'])
def get_drivers():
    updated_drivers = []
    for driver in data['drivers']:
        updated_drivers.append(check_status(driver))
    return jsonify(updated_drivers)

@app.route('/drivers/<license_id>', methods=['GET'])
def get_driver(license_id):
    driver = next((d for d in data['drivers'] if d['license_id'] == license_id), None)
    if driver:
        return jsonify(check_status(driver))
    return jsonify({'message': 'Driver not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
