import mediapipe as mp

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

    def get_gesture(self, hand_landmarks):
        tips = [
            self.mp_hands.HandLandmark.THUMB_TIP,
            self.mp_hands.HandLandmark.INDEX_FINGER_TIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP,
            self.mp_hands.HandLandmark.RING_FINGER_TIP,
            self.mp_hands.HandLandmark.PINKY_TIP
        ]
        
        pips = [
            self.mp_hands.HandLandmark.THUMB_IP,
            self.mp_hands.HandLandmark.INDEX_FINGER_PIP,
            self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP,
            self.mp_hands.HandLandmark.RING_FINGER_PIP,
            self.mp_hands.HandLandmark.PINKY_PIP
        ]

        fingers_up = []
        
        thumb_tip = hand_landmarks.landmark[tips[0]]
        thumb_ip = hand_landmarks.landmark[pips[0]]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        
        if abs(thumb_tip.x - index_mcp.x) > abs(thumb_ip.x - index_mcp.x):
            fingers_up.append(1)
        else:
            fingers_up.append(0)

        for i in range(1, 5):
            tip = hand_landmarks.landmark[tips[i]]
            pip = hand_landmarks.landmark[pips[i]]
            if tip.y < pip.y:
                fingers_up.append(1)
            else:
                fingers_up.append(0)

        if fingers_up == [0, 1, 0, 0, 0]:
            return "INDEX ONLY"
        elif fingers_up == [1, 1, 1, 1, 1] or fingers_up == [0, 1, 1, 1, 1]:
            return "OPEN PALM"
        elif fingers_up == [0, 0, 0, 0, 0]:
            return "FIST"
        elif fingers_up == [1, 0, 0, 0, 0]:
            return "THUMBS UP"
        elif fingers_up == [0, 0, 0, 0, 1]:
            return "PINKY ONLY" # Nhận diện cử chỉ móc ngoéo ngón út
        else:
            return "UNKNOWN"