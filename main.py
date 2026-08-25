import cv2
import mediapipe as mp
import time
import math
from gesture import GestureDetector
from drawing import DrawingCanvas
from recognizer import ExpressionRecognizer
from calculator import SafeCalculator

def main():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FPS, 144)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    detector = GestureDetector()
    canvas = DrawingCanvas(width, height)
    recognizer = ExpressionRecognizer()
    calculator = SafeCalculator()
    mp_drawing = mp.solutions.drawing_utils

    state = "READY"
    dual_state = "NONE" 
    
    expression = "-"
    result = "-"
    prev_time = time.time()
    gesture_buffer = []

    print("Hiếu thân mến, phiên bản hoàn toàn sạch sẽ đã sẵn sàng!")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = detector.hands.process(rgb_frame)
        current_gesture = "NONE"
        is_dual_mode_active = False

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, detector.mp_hands.HAND_CONNECTIONS)

            # -------------------------------------------------------------
            # PHẦN 1: TÍNH NĂNG 2 TAY (VẼ HÌNH ĐẶC BIỆT - KHÔNG CÓ CHẤM MÀU)
            # -------------------------------------------------------------
            if len(results.multi_hand_landmarks) == 2:
                hand1 = results.multi_hand_landmarks[0]
                hand2 = results.multi_hand_landmarks[1]

                idx1 = (int(hand1.landmark[8].x * width), int(hand1.landmark[8].y * height))
                thb1 = (int(hand1.landmark[4].x * width), int(hand1.landmark[4].y * height))
                pnk1 = (int(hand1.landmark[20].x * width), int(hand1.landmark[20].y * height))

                idx2 = (int(hand2.landmark[8].x * width), int(hand2.landmark[8].y * height))
                thb2 = (int(hand2.landmark[4].x * width), int(hand2.landmark[4].y * height))
                pnk2 = (int(hand2.landmark[20].x * width), int(hand2.landmark[20].y * height))

                dist_index = math.hypot(idx1[0] - idx2[0], idx1[1] - idx2[1])
                dist_rect1 = math.hypot(idx1[0] - thb2[0], idx1[1] - thb2[1])
                dist_rect2 = math.hypot(idx2[0] - thb1[0], idx2[1] - thb1[1])
                dist_pnk   = math.hypot(pnk1[0] - pnk2[0], pnk1[1] - pnk2[1])

                TRIGGER_DIST = 90

                if dist_index < TRIGGER_DIST: dual_state = "LINKING"
                elif dist_rect1 < TRIGGER_DIST: dual_state = "RECTANGLE_12"
                elif dist_rect2 < TRIGGER_DIST: dual_state = "RECTANGLE_21"
                elif dist_pnk < TRIGGER_DIST: dual_state = "CIRCLE"  

                if dual_state != "NONE":
                    is_dual_mode_active = True 

                if dual_state == "LINKING":
                    cv2.line(frame, idx1, idx2, (255, 105, 180), 8)
                    cv2.putText(frame, "LINKING MODE", (width//2 - 100, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 105, 180), 3)
                elif dual_state == "RECTANGLE_12":
                    cv2.rectangle(frame, idx1, thb2, (0, 255, 255), 6)
                    cv2.putText(frame, "RECTANGLE MODE", (width//2 - 130, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                elif dual_state == "RECTANGLE_21":
                    cv2.rectangle(frame, idx2, thb1, (0, 255, 255), 6)
                    cv2.putText(frame, "RECTANGLE MODE", (width//2 - 130, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
                elif dual_state == "CIRCLE":
                    center_x, center_y = (pnk1[0] + pnk2[0]) // 2, (pnk1[1] + pnk2[1]) // 2
                    radius = int(dist_pnk / 2)
                    radius = max(radius, 25) 
                    
                    # Chỉ vẽ hình tròn màu xanh lá, KHÔNG CÓ CHẤM ĐỎ Ở TÂM NỮA
                    cv2.circle(frame, (center_x, center_y), radius, (0, 255, 0), 6)
                    cv2.putText(frame, "CIRCLE MODE (PINKY)", (width//2 - 150, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)
            else:
                dual_state = "NONE"

            # -------------------------------------------------------------
            # PHẦN 2: VIẾT SỐ & TÍNH TOÁN BẰNG 1 TAY (Ngón Trỏ)
            # -------------------------------------------------------------
            first_hand = results.multi_hand_landmarks[0]
            raw_gesture = detector.get_gesture(first_hand)
            
            if raw_gesture == "INDEX ONLY":
                current_gesture = "INDEX ONLY"
            else:
                gesture_buffer.append(raw_gesture)
                if len(gesture_buffer) > 3: gesture_buffer.pop(0)
                if gesture_buffer.count(raw_gesture) >= 2: current_gesture = raw_gesture

            if not is_dual_mode_active:
                if current_gesture == "INDEX ONLY":
                    state = "DRAWING"
                    idx_tip = first_hand.landmark[detector.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                    canvas.update(int(idx_tip.x * width), int(idx_tip.y * height))
                elif current_gesture == "FIST" or current_gesture == "PINKY ONLY":
                    if state in ["DRAWING", "PAUSED"]:
                        state = "PAUSED"
                        canvas.pause()
                elif current_gesture == "OPEN PALM":
                    state = "READY"
                    canvas.clear()
                    expression, result = "-", "-"
                elif current_gesture == "THUMBS UP":
                    if state in ["DRAWING", "PAUSED", "READY"]:
                        state = "CALCULATING"
                        canvas.pause()
                        expression = recognizer.recognize(canvas.canvas)
                        if expression and expression != "Tesseract Error":
                            result = calculator.evaluate(expression)
                        else:
                            result = expression
                        state = "RESULT"
            else:
                canvas.pause()
                state = "DUAL SHAPE"

        else:
            current_gesture = "NO HAND"
            dual_state = "NONE"
            canvas.pause()

        final_frame = canvas.get_overlay(frame)

        curr_time = time.time()
        fps = int(1 / (curr_time - prev_time + 0.0001))
        prev_time = curr_time

        cv2.putText(final_frame, f"FPS: {fps}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(final_frame, f"Mode: {state}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(final_frame, f"Gesture: {current_gesture}", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        cv2.rectangle(final_frame, (width - 350, 10), (width - 10, 100), (0, 0, 0), -1)
        cv2.putText(final_frame, f"Expr: {expression}", (width - 340, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(final_frame, f"Result: {result}", (width - 340, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow("Hieu's AI Calculator", final_frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break
        elif key == ord('c'):
            canvas.clear()
            expression, result = "-", "-"
            state = "READY"
            dual_state = "NONE"

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()