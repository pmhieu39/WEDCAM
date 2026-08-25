# Hand Drawing Calculator 🧮🤚

Một dự án AI Computer Vision cho phép người dùng viết các biểu thức toán học trong không khí bằng ngón trỏ và hệ thống sẽ tự động giải nó.

## Tính năng
- ✍️ **Viết tự do:** Dùng ngón trỏ để viết số và dấu (+, -, *, /).
- 🧠 **Smart Gestures:** Xòe tay để xóa, Nắm tay để dừng vẽ, Giơ ngón cái để tính toán.
- 🧮 **Safe Math Engine:** Sử dụng Abstract Syntax Tree (AST) không dùng `eval()` để đảm bảo an toàn.

## Yêu cầu
- Python 3.10+
- Camera (Webcam)
- Tesseract OCR for Windows (Tải tại https://github.com/UB-Mannheim/tesseract/wiki)

## Cài đặt nhanh
1. Tạo môi trường ảo: `python -m venv venv`
2. Kích hoạt môi trường: `venv\Scripts\activate`
3. Cài thư viện: `pip install opencv-python mediapipe numpy pytesseract`
4. Chạy game: `python main.py`

## Các cử chỉ hỗ trợ
* **INDEX ONLY (Chỉ ngón trỏ duỗi):** Kích hoạt bút vẽ `DRAWING`.
* **FIST (Nắm đấm):** Tạm dừng bút vẽ `PAUSED`.
* **OPEN PALM (Xòe 5 ngón):** Xóa toàn bộ canvas và reset kết quả `CANCEL`.
* **THUMBS UP (Giơ ngón cái):** Chốt biểu thức và tiến hành nhận diện `CALCULATE`.

## Phím tắt bàn phím
- `Q` hoặc `ESC`: Thoát chương trình.
- `C`: Xóa nhanh (Clear).