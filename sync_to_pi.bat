@echo off
chcp 65001 >nul
echo =======================================================
echo   SMART CART - ĐỒNG BỘ CODE TỪ PC SANG RASPBERRY PI
echo =======================================================
echo Đang sao chép code sang Raspberry Pi (192.168.57.153)...

scp app.py admin.html index.html .env schema.sql start_kiosk.sh qrcode.min.js barcode_scanner_min.js pi@192.168.57.153:/home/pi/smartcart/

if %ERRORLEVEL% equ 0 (
    echo =======================================================
    echo ✓ Đồng bộ thành công tất cả file sang Raspberry Pi!
    echo =======================================================
) else (
    echo =======================================================
    echo ❌ Lỗi kết nối tới Pi! Vui lòng kiểm tra:
    echo 1. Pi đã cắm nguồn và khởi động xong chưa?
    echo 2. PC và Pi có đang bắt chung mạng Wi-Fi không?
    echo 3. Địa chỉ IP của Pi có đúng là 192.168.57.153 không?
    echo =======================================================
)
pause

