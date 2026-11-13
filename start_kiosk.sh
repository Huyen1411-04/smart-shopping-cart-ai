#!/bin/bash
# =============================================================
# SMART CART - KIOSK LAUNCHER CHO MÀN HÌNH 7" 800x480
# =============================================================

# Đảm bảo hiển thị lên màn hình vật lý
export DISPLAY="${DISPLAY:-:0}"

# Đóng mọi tiến trình Chromium đang mở trước đó để chuyển hẳn sang Kiosk độc lập
killall -9 chromium chromium-browser 2>/dev/null
sleep 1

# Tắt chế độ tắt màn hình / screensaver / ngủ màn hình
xset s off 2>/dev/null
xset -dpms 2>/dev/null
xset s noblank 2>/dev/null

# Bật hiển thị con trỏ chuột (khôi phục con trỏ mũi tên mặc định)
killall unclutter 2>/dev/null
xsetroot -cursor_name left_ptr 2>/dev/null

# =============================================================
# CẤU HÌNH XOAY MÀN HÌNH & ÁNH XẠ CẢM ỨNG
# Mặc định chuẩn màn hình ngang 7" (800x480: "normal")
# Có thể truyền tham số nếu cần xoay dọc: ./start_kiosk.sh right hoặc left
# =============================================================
ROTATION="${1:-normal}"
TOUCH_DEVICE="10-0038 generic ft5x06 (00)"

if [ "$ROTATION" = "right" ]; then
    # Xoay dọc 90 độ theo chiều kim đồng hồ
    for out in DSI-1 HDMI-1 HDMI-2; do
        xrandr --output "$out" --rotate right 2>/dev/null
    done
    xinput set-prop "$TOUCH_DEVICE" "Coordinate Transformation Matrix" 0 1 0 -1 0 1 0 0 1 2>/dev/null
    WIN_SIZE="480,800"
    SCALE="1.0"
elif [ "$ROTATION" = "left" ]; then
    # Xoay dọc ngược lại 270 độ (nếu cắm cáp ngược)
    for out in DSI-1 HDMI-1 HDMI-2; do
        xrandr --output "$out" --rotate left 2>/dev/null
    done
    xinput set-prop "$TOUCH_DEVICE" "Coordinate Transformation Matrix" 0 -1 1 1 0 0 0 0 1 2>/dev/null
    WIN_SIZE="480,800"
    SCALE="1.0"
else
    # Mặc định chuẩn màn hình ngang 7" 800x480
    for out in DSI-1 HDMI-1 HDMI-2; do
        xrandr --output "$out" --rotate normal 2>/dev/null
    done
    xinput set-prop "$TOUCH_DEVICE" "Coordinate Transformation Matrix" 1 0 0 0 1 0 0 0 1 2>/dev/null
    WIN_SIZE="800,480"
    SCALE="1.0"
fi

# Khởi động Flask backend nếu chưa chạy
pkill -9 -f "python.*app.py" 2>/dev/null; sleep 1; if true; then
    cd /home/pi/smartcart
    /home/pi/smartcart/venv/bin/python -u app.py > /home/pi/smartcart/app.log 2>&1 &
fi

# Chờ Flask server mở cổng 8080 sẵn sàng
until curl -s http://localhost:8080 > /dev/null; do
    sleep 1
done

# Khởi động Ngrok Tunnel ngầm với tên miền cố định nếu chưa chạy
if ! pgrep -x "ngrok" > /dev/null; then
    ngrok http --url=unabetted-babette-ungleefully.ngrok-free.dev 8080 > /home/pi/smartcart/ngrok.log 2>&1 &
fi

# Tạo thư mục profile riêng cho Kiosk (tránh xung đột với trình duyệt thường)
KIOSK_DATA_DIR="/home/pi/.config/chromium-kiosk"
mkdir -p "$KIOSK_DATA_DIR/Default"

# Xóa cảnh báo "Chromium didn't shut down correctly" nếu bị tắt nguồn đột ngột
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' "$KIOSK_DATA_DIR/Default/Preferences" 2>/dev/null
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' "$KIOSK_DATA_DIR/Default/Preferences" 2>/dev/null

# Chạy Chromium chế độ Kiosk toàn màn hình vừa khít màn hình dọc 480x800
exec chromium \
  --kiosk \
  --user-data-dir="$KIOSK_DATA_DIR" \
  --noerrdialogs \
  --disable-infobars \
  --disable-features=Translate \
  --disable-translate \
  --no-first-run \
  --check-for-update-interval=31536000 \
  --disable-pinch \
  --overscroll-history-navigation=0 \
  --enable-features=OverlayScrollbar \
  --touch-events=enabled \
  --remote-debugging-port=9222 \
  --force-device-scale-factor=$SCALE \
  --window-size=$WIN_SIZE \
  --window-position=0,0 \
  http://localhost:8080
