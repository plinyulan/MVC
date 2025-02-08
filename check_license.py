# เช็คข้อมูลของผู้ขับขี่
import json

# โหลดข้อมูลผู้ขับขี่จากไฟล์ JSON
def load_data():
    with open("drivers.json", "r", encoding="utf-8") as file:
        return json.load(file)["drivers"]

# ตรวจสอบใบขับขี่
def validate_license(license_id):
    # ตรวจสอบว่าหมายเลขใบขับขี่มี 9 หลักและไม่ขึ้นต้นด้วย 0
    if not license_id.isdigit() or len(license_id) != 9 or license_id[0] == '0':
        return " หมายเลขใบขับขี่ไม่ถูกต้อง (ต้องเป็นเลข 9 หลักและไม่ขึ้นต้นด้วย 0)"
    
    # โหลดฐานข้อมูล
    drivers = load_data()
    
    # ค้นหาข้อมูลผู้ขับขี่
    for driver in drivers:
        if driver["license_id"] == license_id:
            # ข้อมูลของผู้ขับขี่
            info = (
                f" พบข้อมูลผู้ขับขี่\n"
                f" หมายเลขใบขับขี่: {driver['license_id']}\n"
                f" ประเภท: {driver['type']}\n"
                f" วันเกิด: {driver['birthdate']}\n"
                f" สถานะ: {driver['status']}\n"
            )
            # ถ้าเป็น "คนขับรถสาธารณะ" ให้แสดงจำนวนการร้องเรียน
            if driver["type"] == "คนขับรถสาธารณะ":
                info += f" จำนวนร้องเรียน: {driver.get('complaints', 0)} ครั้ง"
            return info
    
    # ถ้าไม่พบหมายเลขใบขับขี่
    return " ไม่พบหมายเลขใบขับขี่ในระบบ"

# ทดสอบโปรแกรม
if __name__ == "__main__":
    user_input = input(" ป้อนหมายเลขใบขับขี่: ")
    print(validate_license(user_input))

