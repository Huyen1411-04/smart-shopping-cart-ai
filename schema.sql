-- Schema cho database smart_cart_db (Smart Cart project)
-- Tạo dựa theo các cột mà app.py thực sự sử dụng trong các câu SQL

CREATE TABLE IF NOT EXISTS products (
    barcode VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    stock_quantity INT NOT NULL DEFAULT 0,
    icon VARCHAR(20) DEFAULT '📦',
    counter VARCHAR(100) NOT NULL,
    weight DECIMAL(10,2) DEFAULT 0,
    embedding LONGTEXT DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    device_source VARCHAR(50),
    subtotal_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    points_used INT NOT NULL DEFAULT 0,
    discount_amount DECIMAL(12,2) NOT NULL DEFAULT 0,
    total_amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    member_phone VARCHAR(20) DEFAULT NULL,
    customer_email VARCHAR(255) DEFAULT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    barcode VARCHAR(50) NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (barcode) REFERENCES products(barcode)
);

CREATE TABLE IF NOT EXISTS members (
    phone_number VARCHAR(20) PRIMARY KEY,
    face_image_path VARCHAR(500),
    points INT NOT NULL DEFAULT 0,
    face_encoding LONGTEXT DEFAULT NULL
);
