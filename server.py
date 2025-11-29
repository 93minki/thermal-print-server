from flask import Flask, request, jsonify
from flask_cors import CORS
import win32print
import win32ui

app = Flask(__name__)

# CORS 설정을 더 명시적으로 설정
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow-headers": ["Content-Type", "Authorization"]
    }
})

def print_order(order_number: str):
    printer_name = win32print.GetDefaultPrinter()
    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)
    hDC.StartDoc("Order Print")
    hDC.StartPage()
    
    PRINT_WIDTH = 384
    font_size = 260
    
    # 주문번호 폰트 크기 계산 (기존 로직 유지)
    while True:
        font = win32ui.CreateFont({
            "name": "Arial",
            "height": font_size,
            "weight": 700,
        })
        hDC.SelectObject(font)
        text_w, text_h = hDC.GetTextExtent(order_number)
        if text_w <= PRINT_WIDTH:
            break
        font_size -= 10
        if font_size < 80:
            break
    
    # 작은 폰트 크기 설정 (주문번호 폰트의 약 1/3)
    small_font_size = max(60, font_size // 5)
    
    x = 0
    y = 50
    
    # 1. "주문번호" 텍스트 출력 (작은 폰트)
    small_font = win32ui.CreateFont({
        "name": "Arial",
        "height": small_font_size,
        "weight": 400,
    })
    hDC.SelectObject(small_font)
    _, label_h = hDC.GetTextExtent("주문번호")
    hDC.TextOut(x, y, "주문번호")
    
    # 2. 주문번호 출력 (큰 폰트)
    y += label_h + 30  # 여백 추가
    order_font = win32ui.CreateFont({
        "name": "Arial",
        "height": font_size,
        "weight": 700,
    })
    hDC.SelectObject(order_font)
    _, order_h = hDC.GetTextExtent(order_number)
    hDC.TextOut(x, y, order_number)
    
    # 3. "달리는 푸드카페" 텍스트 출력 (작은 폰트)
    y += order_h + 30  # 여백 추가
    hDC.SelectObject(small_font)
    hDC.TextOut(x, y, "달리는 푸드카페")
    
    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

@app.post("/print")
def print_api():
    try:
        data = request.get_json()
        print(f"Received request: {data}")  # 디버깅용 로그
        
        if not data or "orderNumber" not in data:
            return jsonify({"error": "order is required"}), 400
        
        order_number = str(data["orderNumber"])
        print(f"Printing order: {order_number}")  # 디버깅용 로그
        
        print_order(order_number)
        return jsonify({"status": "ok", "printed": order_number})
    except Exception as e:
        print(f"Error: {str(e)}")  # 디버깅용 로그
        return jsonify({"error": str(e)}), 500

@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "ok", "message": "Flask server is running"})

if __name__ == "__main__":
    print("Starting Flask server on 0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)

