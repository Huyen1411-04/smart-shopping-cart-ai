@echo off
chcp 65001 >nul
echo =======================================================
echo   SMART CART - RELOAD GIAO DIEN KHACH HANG TREN PI
echo =======================================================
echo Đang gửi tín hiệu reload tới Raspberry Pi (192.168.57.153)...
ssh pi@192.168.57.153 "/home/pi/smartcart/reload_kiosk.sh"
echo =======================================================
echo Hoàn tất!
timeout /t 3
