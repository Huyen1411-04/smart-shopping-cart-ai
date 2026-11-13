import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv("/home/pi/smartcart/.env")

conn = mysql.connector.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "cart_user"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "smart_cart")
)
cursor = conn.cursor()

staples = [
    ("8935001234515", "Thịt bò phi lê tươi 500g", 125000, 30, "Quầy đồ đông lạnh", 500),
    ("8935001234522", "Thịt ba chỉ heo tươi 500g", 85000, 35, "Quầy đồ đông lạnh", 500),
    ("8935001234539", "Cá lóc phi lê làm sạch 500g", 75000, 25, "Quầy đồ đông lạnh", 500),
    ("8935001234546", "Bánh phở tươi gói 500g", 18000, 40, "Quầy đồ đông lạnh", 500),
    ("8935001234553", "Trứng gà tươi Ba Huân (10 quả)", 32000, 50, "Quầy rau củ", 600),
    ("8935001234560", "Thơm (Dứa) gọt sẵn 1 trái", 15000, 30, "Quầy rau củ", 450),
    ("8935001234577", "Gừng củ tươi gói 200g", 12000, 40, "Quầy rau củ", 200),
    ("8935001234584", "Hành lá & ngò rí gói 150g", 10000, 40, "Quầy rau củ", 150),
    ("8935001234591", "Đậu bắp tươi gói 250g", 14000, 35, "Quầy rau củ", 250),
    ("8935001234607", "Gia vị Lẩu Thái Aji-Quick 50g", 9000, 60, "Quầy bánh kẹo", 50),
    ("8935001234614", "Gia vị Nấu Phở Bò Aji-Quick 50g", 9000, 60, "Quầy bánh kẹo", 50),
]

for p in staples:
    cursor.execute("""
        INSERT INTO products (barcode, name, price, stock_quantity, counter, weight, icon)
        VALUES (%s, %s, %s, %s, %s, %s, '')
        ON DUPLICATE KEY UPDATE name = VALUES(name), price = VALUES(price), counter = VALUES(counter), weight = VALUES(weight)
    """, p)

conn.commit()
print(f"Added {len(staples)} essential grocery staples to supermarket inventory!")
cursor.close()
conn.close()
