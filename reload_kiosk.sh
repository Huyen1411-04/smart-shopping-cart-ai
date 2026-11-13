#!/bin/bash
# =============================================================
# SMART CART - SCRIPT RELOAD NHANH GIAO DIEN KIOSK TREN PI
# =============================================================

export DISPLAY="${DISPLAY:-:0}"

# 1. Thu reload nhanh qua Chrome DevTools Port 9222 (khong lam giat hay tat man hinh)
RELOADED=$(/home/pi/smartcart/venv/bin/python -c "
import urllib.request, json, asyncio, websockets
async def reload_page():
    try:
        req = urllib.request.urlopen('http://localhost:9222/json', timeout=2)
        pages = json.loads(req.read().decode())
        page = [p for p in pages if p.get('type') == 'page'][0]
        async with websockets.connect(page['webSocketDebuggerUrl']) as ws:
            await ws.send(json.dumps({'id': 1, 'method': 'Page.reload', 'params': {'ignoreCache': True}}))
            await ws.recv()
        print('SUCCESS')
    except Exception:
        print('FAIL')
asyncio.run(reload_page())
" 2>/dev/null)

if [ "$RELOADED" = "SUCCESS" ]; then
    echo "✓ Da reload lai trang web khach hang thanh cong!"
    exit 0
fi

# 2. Neu Chromium chua bat hoac cong 9222 chua san sang -> Khoi dong lai Kiosk bang start_kiosk.sh
echo "-> Dang khoi dong lai Kiosk Chromium..."
/home/pi/smartcart/start_kiosk.sh > /dev/null 2>&1 &
echo "✓ Da khoi dong lai che do Kiosk thanh cong!"
