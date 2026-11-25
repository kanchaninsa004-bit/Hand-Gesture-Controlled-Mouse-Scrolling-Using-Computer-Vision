import math


class GestureDetector:
    """Detects mouse gestures using hand landmarks."""

    def __init__(self, movement_threshold=12):
        self.previous_y = None
        self.movement_threshold = movement_threshold

    def distance(self, p1, p2):
        """Calculate distance between two points."""
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

    def detect(self, landmarks):
        if not landmarks:
            self.previous_y = None
            return "NO HAND"

        # MediaPipe landmarks:
        # 0  = Wrist
        # 4  = Thumb tip
        # 8  = Index finger tip
        # 12 = Middle finger tip

        wrist_x, wrist_y = landmarks[0]
        thumb_x, thumb_y = landmarks[4]
        index_x, index_y = landmarks[8]
        middle_x, middle_y = landmarks[12]

        # --------------------------------
        # PINCH = thumb + index close
        # --------------------------------
        pinch_distance = self.distance(
            (thumb_x, thumb_y),
            (index_x, index_y)
        )

        if pinch_distance < 40:
            return "CLICK"

        # --------------------------------
        # TWO FINGERS = index + middle
        # --------------------------------
        two_finger_distance = self.distance(
            (index_x, index_y),
            (middle_x, middle_y)
        )

        if two_finger_distance < 50:
            return "RIGHT CLICK"

        # --------------------------------
        # SCROLL
        # --------------------------------
        if self.previous_y is None:
            self.previous_y = wrist_y
            return "NEUTRAL"

        movement = wrist_y - self.previous_y

        self.previous_y = wrist_y

        if movement < -self.movement_threshold:
            return "SCROLL UP"

        if movement > self.movement_threshold:
            return "SCROLL DOWN"

        # --------------------------------
        # INDEX FINGER = MOVE
        # --------------------------------
        return "MOVE"

    def reset(self):
        self.previous_y = None