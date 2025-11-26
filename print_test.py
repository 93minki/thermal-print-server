import win32print
import win32ui
import win32con

def print_order(order_number: str):
    printer_name = win32print.GetDefaultPrinter()

    hDC = win32ui.CreateDC()
    hDC.CreatePrinterDC(printer_name)

    hDC.StartDoc("Order Print")
    hDC.StartPage()

    # 58mm 프린터 실제 출력 폭 (픽셀)
    PRINT_WIDTH = 384   # ← 반드시 이것

    font_size = 260

    while True:
        font = win32ui.CreateFont({
            "name": "Arial",
            "height": font_size,
            "weight": 700,
        })
        hDC.SelectObject(font)

        text_w, text_h = hDC.GetTextExtent(order_number)

        # 폭에 들어가면 멈춤
        if text_w <= PRINT_WIDTH:
            break

        font_size -= 10
        if font_size < 80:
            break

    # 왼쪽 정렬 (중앙 정렬 X)
    x = 0               # ← 이게 핵심
    y = 100             # 세로 위치는 적당히 조정

    hDC.TextOut(x, y, order_number)

    hDC.EndPage()
    hDC.EndDoc()
    hDC.DeleteDC()

if __name__ == "__main__":
    print_order("12345")
