import numpy as np
import cv2

class DrawingCanvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.canvas = np.zeros((height, width, 3), dtype=np.uint8)
        self.prev_x = 0
        self.prev_y = 0
        self.alpha = 0.6  # Hệ số làm mượt (Linear Interpolation/Moving Average)

    def update(self, current_x, current_y):
        # Làm mượt đường vẽ (tránh tay bị rung)
        if self.prev_x == 0 and self.prev_y == 0:
            smooth_x, smooth_y = current_x, current_y
        else:
            smooth_x = int(self.alpha * current_x + (1 - self.alpha) * self.prev_x)
            smooth_y = int(self.alpha * current_y + (1 - self.alpha) * self.prev_y)

        # Vẽ đường nối từ tọa độ cũ đến tọa độ mới (Màu xanh lá, nét dày 8)
        if self.prev_x != 0 and self.prev_y != 0:
            cv2.line(self.canvas, (self.prev_x, self.prev_y), (smooth_x, smooth_y), (0, 255, 0), 8)

        self.prev_x = smooth_x
        self.prev_y = smooth_y

    def pause(self):
        # Reset tọa độ khi tạm dừng để khi vẽ lại không bị nối thành đường chéo
        self.prev_x = 0
        self.prev_y = 0

    def clear(self):
        self.canvas = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.pause()

    def get_overlay(self, frame):
        # Chuyển phần nền đen thành trong suốt để đè lên webcam
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        
        frame_bg = cv2.bitwise_and(frame, frame, mask=mask_inv)
        canvas_fg = cv2.bitwise_and(self.canvas, self.canvas, mask=mask)
        return cv2.add(frame_bg, canvas_fg)