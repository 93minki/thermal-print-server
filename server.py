from flask import Flask, request, jsonify
from flask_cors import CORS
import win32print
import win32ui

app = Flask(__name__)
CORS(app)  # ← 이 한 줄이 브라우저 요청 모두 허용

def print_order(order_number: str):
    printer_name = win32print.GetDefaultPrinter()

    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    hDC.StartDoc("Order Print")
    hDC.StartPage()

    PRINT_WIDTH = 384
    font_size = 260

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

    x = 0
    y = 100

    hDC.TextOut(x, y, order_number)

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()


@app.post("/print")
def print_api():
    data = request.get_json()

    if not data or "order" not in data:
        return jsonify({"error": "order is required"}), 400

    order_number = str(data["order"])

    try:
        print_order(order_number)
        return jsonify({"status": "ok", "printed": order_number})
    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run(port=5000, debug=True)
