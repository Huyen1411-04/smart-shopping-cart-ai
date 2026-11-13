# -*- coding: utf-8 -*-
"""
Smart Cart - Script bổ sung 40 sản phẩm siêu thị phong phú vào cơ sở dữ liệu.
Bao gồm: Mã vạch chuẩn (EAN-13), tên sản phẩm, giá bán, số lượng tồn kho,
khối lượng chính xác (dành cho cảm biến cân load cell), biểu tượng icon, và quầy hàng.
"""

import os
import mysql.connector

PRODUCTS_TO_ADD = [
    # =========================================================
    # 1. QUẦY ĐỒ UỐNG (10 sản phẩm)
    # =========================================================
    {
        "barcode": "8934822212002",
        "name": "Bia Heineken Sleek lon 330ml",
        "price": 21000,
        "stock_quantity": 100,
        "counter": "Quầy đồ uống",
        "weight": 350.0,
        "icon": "🍺",
        "ingredient_key": "bia_heineken",
        "net_quantity": 330,
        "net_unit": "ml"
    },
    {
        "barcode": "8934822122332",
        "name": "Bia Tiger Crystal lon 330ml",
        "price": 19000,
        "stock_quantity": 100,
        "counter": "Quầy đồ uống",
        "weight": 350.0,
        "icon": "🍺",
        "ingredient_key": "bia_tiger",
        "net_quantity": 330,
        "net_unit": "ml"
    },
    {
        "barcode": "8934565000018",
        "name": "Bia 333 lon 330ml",
        "price": 14000,
        "stock_quantity": 120,
        "counter": "Quầy đồ uống",
        "weight": 350.0,
        "icon": "🍺",
        "ingredient_key": "bia_333",
        "net_quantity": 330,
        "net_unit": "ml"
    },
    {
        "barcode": "8934673121018",
        "name": "Sữa chua uống Vinamilk Susu dâu 110ml",
        "price": 7000,
        "stock_quantity": 150,
        "counter": "Quầy đồ uống",
        "weight": 125.0,
        "icon": "🥛",
        "ingredient_key": "sua_chua_uong",
        "net_quantity": 110,
        "net_unit": "ml"
    },
    {
        "barcode": "8934804021202",
        "name": "Thức uống lúa mạch Nestlé Milo 180ml",
        "price": 11000,
        "stock_quantity": 120,
        "counter": "Quầy đồ uống",
        "weight": 200.0,
        "icon": "🍫",
        "ingredient_key": "milo",
        "net_quantity": 180,
        "net_unit": "ml"
    },
    {
        "barcode": "8934804005011",
        "name": "Sữa tươi Dutch Lady có đường 180ml",
        "price": 9000,
        "stock_quantity": 100,
        "counter": "Quầy đồ uống",
        "weight": 195.0,
        "icon": "🥛",
        "ingredient_key": "sua_tuoi",
        "net_quantity": 180,
        "net_unit": "ml"
    },
    {
        "barcode": "8934804002157",
        "name": "Trà chanh Nestea túi 18 gói x 14g",
        "price": 38000,
        "stock_quantity": 50,
        "counter": "Quầy đồ uống",
        "weight": 260.0,
        "icon": "🍵",
        "ingredient_key": "tra_chanh",
        "net_quantity": 252,
        "net_unit": "g"
    },
    {
        "barcode": "8935049500016",
        "name": "Trà xanh Không Độ 455ml",
        "price": 10000,
        "stock_quantity": 80,
        "counter": "Quầy đồ uống",
        "weight": 480.0,
        "icon": "🍵",
        "ingredient_key": "tra_xanh",
        "net_quantity": 455,
        "net_unit": "ml"
    },
    {
        "barcode": "8934804011128",
        "name": "Cà phê sữa đá Nescafé hộp 20 gói",
        "price": 55000,
        "stock_quantity": 60,
        "counter": "Quầy đồ uống",
        "weight": 350.0,
        "icon": "☕",
        "ingredient_key": "ca_phe_nescafe",
        "net_quantity": 320,
        "net_unit": "g"
    },
    {
        "barcode": "8935246700012",
        "name": "Nước dừa tươi Cocoxim xiêm xanh 330ml",
        "price": 16000,
        "stock_quantity": 75,
        "counter": "Quầy đồ uống",
        "weight": 360.0,
        "icon": "🥥",
        "ingredient_key": "nuoc_dua",
        "net_quantity": 330,
        "net_unit": "ml"
    },

    # =========================================================
    # 2. QUẦY BÁNH KẸO & ĐỒ KHÔ ĂN LIỀN (10 sản phẩm)
    # =========================================================
    {
        "barcode": "8934563138164",
        "name": "Mì Hảo Hảo tôm chua cay 75g",
        "price": 4500,
        "stock_quantity": 200,
        "counter": "Quầy bánh kẹo",
        "weight": 80.0,
        "icon": "🍜",
        "ingredient_key": "mi_hao_hao",
        "net_quantity": 75,
        "net_unit": "g"
    },
    {
        "barcode": "8936017362489",
        "name": "Mì Omachi sườn hầm ngũ quả 80g",
        "price": 8500,
        "stock_quantity": 150,
        "counter": "Quầy bánh kẹo",
        "weight": 88.0,
        "icon": "🍜",
        "ingredient_key": "mi_omachi",
        "net_quantity": 80,
        "net_unit": "g"
    },
    {
        "barcode": "8936017360010",
        "name": "Tương ớt Chin-su chai 250g",
        "price": 14000,
        "stock_quantity": 80,
        "counter": "Quầy bánh kẹo",
        "weight": 280.0,
        "icon": "🌶️",
        "ingredient_key": "tuong_ot",
        "net_quantity": 250,
        "net_unit": "g"
    },
    {
        "barcode": "8934680011012",
        "name": "Dầu ăn Tường An Cooking Oil 1L",
        "price": 48000,
        "stock_quantity": 60,
        "counter": "Quầy bánh kẹo",
        "weight": 950.0,
        "icon": "🍳",
        "ingredient_key": "dau_an",
        "net_quantity": 1,
        "net_unit": "L"
    },
    {
        "barcode": "8936017360256",
        "name": "Nước mắm Nam Ngư Đệ Nhị 900ml",
        "price": 32000,
        "stock_quantity": 70,
        "counter": "Quầy bánh kẹo",
        "weight": 1100.0,
        "icon": "🐟",
        "ingredient_key": "nuoc_mam",
        "net_quantity": 900,
        "net_unit": "ml"
    },
    {
        "barcode": "8934868132043",
        "name": "Hạt nêm Knorr thịt thăn xương tủy 400g",
        "price": 36000,
        "stock_quantity": 65,
        "counter": "Quầy bánh kẹo",
        "weight": 410.0,
        "icon": "🧂",
        "ingredient_key": "hat_nem",
        "net_quantity": 400,
        "net_unit": "g"
    },
    {
        "barcode": "8992771000100",
        "name": "Bánh quy bơ Danisa hộp thiếc 454g",
        "price": 135000,
        "stock_quantity": 30,
        "counter": "Quầy bánh kẹo",
        "weight": 650.0,
        "icon": "🍪",
        "ingredient_key": "banh_danisa",
        "net_quantity": 454,
        "net_unit": "g"
    },
    {
        "barcode": "8996001303244",
        "name": "Bánh xốp Cal Cheese Nabati 170g",
        "price": 19000,
        "stock_quantity": 85,
        "counter": "Quầy bánh kẹo",
        "weight": 180.0,
        "icon": "🧀",
        "ingredient_key": "banh_xop",
        "net_quantity": 170,
        "net_unit": "g"
    },
    {
        "barcode": "8935001700010",
        "name": "Kẹo caramen Alpenliebe thỏi 110g",
        "price": 12000,
        "stock_quantity": 90,
        "counter": "Quầy bánh kẹo",
        "weight": 115.0,
        "icon": "🍬",
        "ingredient_key": "keo_alpenliebe",
        "net_quantity": 110,
        "net_unit": "g"
    },
    {
        "barcode": "8851007010156",
        "name": "Snack rong biển cuộn Big Roll vị mực nướng",
        "price": 11000,
        "stock_quantity": 100,
        "counter": "Quầy bánh kẹo",
        "weight": 15.0,
        "icon": "🍘",
        "ingredient_key": "rong_bien",
        "net_quantity": 10.8,
        "net_unit": "g"
    },

    # =========================================================
    # 3. QUẦY ĐỒ ĐÔNG LẠNH & LÀM MÁT (10 sản phẩm)
    # =========================================================
    {
        "barcode": "8936017367897",
        "name": "Xúc xích tiệt trùng Ponnie heo 175g",
        "price": 22000,
        "stock_quantity": 80,
        "counter": "Quầy đồ đông lạnh",
        "weight": 180.0,
        "icon": "🌭",
        "ingredient_key": "xuc_xich_ponnie",
        "net_quantity": 175,
        "net_unit": "g"
    },
    {
        "barcode": "8934561005116",
        "name": "Xúc xích tiệt trùng Vissan heo 175g",
        "price": 20000,
        "stock_quantity": 80,
        "counter": "Quầy đồ đông lạnh",
        "weight": 180.0,
        "icon": "🌭",
        "ingredient_key": "xuc_xich_vissan",
        "net_quantity": 175,
        "net_unit": "g"
    },
    {
        "barcode": "8935217400010",
        "name": "Phô mai Con Bò Cười hộp 8 miếng 112g",
        "price": 39000,
        "stock_quantity": 50,
        "counter": "Quầy đồ đông lạnh",
        "weight": 130.0,
        "icon": "🧀",
        "ingredient_key": "pho_mai",
        "net_quantity": 112,
        "net_unit": "g"
    },
    {
        "barcode": "8936034130016",
        "name": "Đậu hũ non ICHIBAN hộp 220g",
        "price": 11000,
        "stock_quantity": 60,
        "counter": "Quầy đồ đông lạnh",
        "weight": 230.0,
        "icon": "🧊",
        "ingredient_key": "dau_hu_non",
        "net_quantity": 220,
        "net_unit": "g"
    },
    {
        "barcode": "8936036020018",
        "name": "Kim chi cải thảo cắt lát Bibigo 500g",
        "price": 45000,
        "stock_quantity": 45,
        "counter": "Quầy đồ đông lạnh",
        "weight": 520.0,
        "icon": "🥗",
        "ingredient_key": "kim_chi",
        "net_quantity": 500,
        "net_unit": "g"
    },
    {
        "barcode": "8934561001125",
        "name": "Chả lụa que heo Vissan 200g",
        "price": 38000,
        "stock_quantity": 40,
        "counter": "Quầy đồ đông lạnh",
        "weight": 210.0,
        "icon": "🥩",
        "ingredient_key": "cha_lua",
        "net_quantity": 200,
        "net_unit": "g"
    },
    {
        "barcode": "8934673100013",
        "name": "Sữa chua ăn Vinamilk có đường lốc 4 hộp",
        "price": 28000,
        "stock_quantity": 60,
        "counter": "Quầy đồ đông lạnh",
        "weight": 420.0,
        "icon": "🥣",
        "ingredient_key": "sua_chua_an",
        "net_quantity": 400,
        "net_unit": "g"
    },
    {
        "barcode": "8935246800019",
        "name": "Bơ lạt tự nhiên TH True Butter 100g",
        "price": 35000,
        "stock_quantity": 35,
        "counter": "Quầy đồ đông lạnh",
        "weight": 105.0,
        "icon": "🧈",
        "ingredient_key": "bo_lat",
        "net_quantity": 100,
        "net_unit": "g"
    },
    {
        "barcode": "8936055100012",
        "name": "Thanh cua tuyết đông lạnh Mayumi 250g",
        "price": 52000,
        "stock_quantity": 40,
        "counter": "Quầy đồ đông lạnh",
        "weight": 260.0,
        "icon": "🦀",
        "ingredient_key": "thanh_cua",
        "net_quantity": 250,
        "net_unit": "g"
    },
    {
        "barcode": "8934868090011",
        "name": "Kem que Cornetto socola dâu Wall's",
        "price": 17000,
        "stock_quantity": 70,
        "counter": "Quầy đồ đông lạnh",
        "weight": 80.0,
        "icon": "🍦",
        "ingredient_key": "kem_cornetto",
        "net_quantity": 65,
        "net_unit": "ml"
    },

    # =========================================================
    # 4. QUẦY RAU CỦ & TRÁI CÂY TƯƠI (10 sản phẩm)
    # =========================================================
    {
        "barcode": "8935001234701",
        "name": "Táo Envy New Zealand túi 3 trái",
        "price": 85000,
        "stock_quantity": 30,
        "counter": "Quầy rau củ",
        "weight": 600.0,
        "icon": "🍎",
        "ingredient_key": "tao_envy",
        "net_quantity": 600,
        "net_unit": "g"
    },
    {
        "barcode": "8935001234702",
        "name": "Chuối già Nam Mỹ nải tươi",
        "price": 25000,
        "stock_quantity": 40,
        "counter": "Quầy rau củ",
        "weight": 1000.0,
        "icon": "🍌",
        "ingredient_key": "chuoi_gia",
        "net_quantity": 1,
        "net_unit": "kg"
    },
    {
        "barcode": "8935001234703",
        "name": "Cam sành miền Tây túi 1kg",
        "price": 30000,
        "stock_quantity": 40,
        "counter": "Quầy rau củ",
        "weight": 1000.0,
        "icon": "🍊",
        "ingredient_key": "cam_sanh",
        "net_quantity": 1,
        "net_unit": "kg"
    },
    {
        "barcode": "8935001234704",
        "name": "Dưa hấu không hạt Mặt Trời Đỏ",
        "price": 38000,
        "stock_quantity": 25,
        "counter": "Quầy rau củ",
        "weight": 2000.0,
        "icon": "🍉",
        "ingredient_key": "dua_hau",
        "net_quantity": 2,
        "net_unit": "kg"
    },
    {
        "barcode": "8935001234705",
        "name": "Xoài cát Chu chín vàng trái",
        "price": 22000,
        "stock_quantity": 35,
        "counter": "Quầy rau củ",
        "weight": 450.0,
        "icon": "🥭",
        "ingredient_key": "xoai_cat_chu",
        "net_quantity": 450,
        "net_unit": "g"
    },
    {
        "barcode": "8935001234706",
        "name": "Nho xanh không hạt Ninh Thuận hộp 500g",
        "price": 55000,
        "stock_quantity": 30,
        "counter": "Quầy rau củ",
        "weight": 520.0,
        "icon": "🍇",
        "ingredient_key": "nho_xanh",
        "net_quantity": 500,
        "net_unit": "g"
    },
    {
        "barcode": "8809153540019",
        "name": "Nấm kim châm Hàn Quốc gói 150g",
        "price": 13000,
        "stock_quantity": 60,
        "counter": "Quầy rau củ",
        "weight": 155.0,
        "icon": "🍄",
        "ingredient_key": "nam_kim_cham",
        "net_quantity": 150,
        "net_unit": "g"
    },
    {
        "barcode": "8935001234707",
        "name": "Bắp cải tím Đà Lạt",
        "price": 26000,
        "stock_quantity": 30,
        "counter": "Quầy rau củ",
        "weight": 750.0,
        "icon": "🥬",
        "ingredient_key": "bap_cai_tim",
        "net_quantity": 750,
        "net_unit": "g"
    },
    {
        "barcode": "8935001234708",
        "name": "Cà chua bi Cherry đỏ túi 250g",
        "price": 18000,
        "stock_quantity": 45,
        "counter": "Quầy rau củ",
        "weight": 260.0,
        "icon": "🍅",
        "ingredient_key": "ca_chua_bi",
        "net_quantity": 250,
        "net_unit": "g"
    },
    {
        "barcode": "8935001234709",
        "name": "Khoai lang mật Đà Lạt túi 1kg",
        "price": 35000,
        "stock_quantity": 40,
        "counter": "Quầy rau củ",
        "weight": 1000.0,
        "icon": "🍠",
        "ingredient_key": "khoai_lang_mat",
        "net_quantity": 1,
        "net_unit": "kg"
    }
]

def run():
    print(f"Bắt đầu nạp {len(PRODUCTS_TO_ADD)} sản phẩm vào cơ sở dữ liệu Smart Cart...")
    db_host = os.getenv("DB_HOST", "localhost")
    db_user = os.getenv("DB_USER", "cart_user")
    db_pass = os.getenv("DB_PASSWORD", "")
    db_name = os.getenv("DB_NAME", "smart_cart")

    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_pass,
        database=db_name
    )
    cursor = conn.cursor()

    # Kiểm tra các cột tồn tại trong bảng products
    cursor.execute("DESCRIBE products")
    cols = [row[0] for row in cursor.fetchall()]
    has_ai_cols = "ingredient_key" in cols and "net_quantity" in cols and "net_unit" in cols

    added_count = 0
    updated_count = 0

    # Cập nhật Vaseline sang quầy hợp lệ nếu đang để quầy cũ
    cursor.execute("UPDATE products SET counter = 'Quầy bánh kẹo' WHERE barcode = '8851932427722' AND counter = 'My pham'")
    conn.commit()

    for p in PRODUCTS_TO_ADD:
        if has_ai_cols:
            sql = """
                INSERT INTO products (barcode, name, price, stock_quantity, counter, weight, icon, ingredient_key, net_quantity, net_unit)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    price = VALUES(price),
                    stock_quantity = VALUES(stock_quantity),
                    counter = VALUES(counter),
                    weight = VALUES(weight),
                    icon = VALUES(icon),
                    ingredient_key = VALUES(ingredient_key),
                    net_quantity = VALUES(net_quantity),
                    net_unit = VALUES(net_unit)
            """
            val = (
                p["barcode"], p["name"], p["price"], p["stock_quantity"],
                p["counter"], p["weight"], p["icon"],
                p.get("ingredient_key"), p.get("net_quantity"), p.get("net_unit")
            )
        else:
            sql = """
                INSERT INTO products (barcode, name, price, stock_quantity, counter, weight, icon)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                    name = VALUES(name),
                    price = VALUES(price),
                    stock_quantity = VALUES(stock_quantity),
                    counter = VALUES(counter),
                    weight = VALUES(weight),
                    icon = VALUES(icon)
            """
            val = (
                p["barcode"], p["name"], p["price"], p["stock_quantity"],
                p["counter"], p["weight"], p["icon"]
            )

        cursor.execute(sql, val)
        if cursor.rowcount == 1:
            added_count += 1
        else:
            updated_count += 1

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM products")
    total_products = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    print(f"✓ Hoàn tất! Đã thêm mới {added_count} và cập nhật {updated_count} sản phẩm.")
    print(f"✓ Tổng số sản phẩm hiện tại trong kho: {total_products} sản phẩm.")

if __name__ == "__main__":
    run()

