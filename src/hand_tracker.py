import cv2
import mediapipe as mp


class HandTracker:
    """Detects and tracks one hand using MediaPipe."""

    def __init__(
        self,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.7,
    ):
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=max_hands,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        )

    def process_frame(self, frame):
        """Detect a hand and return frame + landmark coordinates."""

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = self.hands.process(rgb_frame)

        landmarks = []

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]

            self.mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                self.mp_hands.HAND_CONNECTIONS,
            )

            height, width, _ = frame.shape

            for landmark in hand_landmarks.landmark:
                x = int(landmark.x * width)
                y = int(landmark.y * height)

                landmarks.append((x, y))

        return frame, landmarks

    def close(self):
        self.hands.close()