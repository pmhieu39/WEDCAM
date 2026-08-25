import cv2
import numpy as np
import pytesseract
import os

# Chỉ định đường dẫn Tesseract trên Windows
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ExpressionRecognizer:
    def __init__(self):
        self.is_ready = os.path.exists(pytesseract.pytesseract.tesseract_cmd)

    def recognize(self, canvas_img):
        if not self.is_ready:
            return "Tesseract Error"

        # Tiền xử lý ảnh để Tesseract dễ đọc hơn
        gray = cv2.cvtColor(canvas_img, cv2.COLOR_BGR2GRAY)
        
        # Làm dày nét vẽ vì tesseract ưu tiên chữ rõ nét
        kernel = np.ones((7,7), np.uint8)
        thick = cv2.dilate(gray, kernel, iterations=1)
        
        # Threshold ảnh
        _, thresh = cv2.threshold(thick, 50, 255, cv2.THRESH_BINARY)
        
        # Invert ảnh (chữ đen nền trắng) vì OCR đọc chữ đen tốt hơn
        inv = cv2.bitwise_not(thresh)

        # Cấu hình OCR: Chỉ nhận diện số và phép toán toán học cơ bản
        # --psm 7: Coi ảnh như 1 dòng văn bản duy nhất
        custom_config = r'--psm 7 -c tessedit_char_whitelist=0123456789+-*/()'
        try:
            text = pytesseract.image_to_string(inv, config=custom_config)
            # Lọc bỏ khoảng trắng thừa
            return text.strip().replace(" ", "")
        except Exception as e:
            return ""