import cv2
import pyautogui

from src.hand_tracker import HandTracker
from src.gesture_detector import GestureDetector


def main():
    camera = cv2.VideoCapture(0)

    if not camera.isOpened():
        print("ERROR: Could not open webcam.")
        return

    tracker = HandTracker()
    gesture_detector = GestureDetector()

    # Screen size
    screen_width, screen_height = pyautogui.size()

    # Cursor smoothing
    smooth_factor = 0.25
    previous_screen_x = screen_width // 2
    previous_screen_y = screen_height // 2

    # Prevent repeated clicks
    left_click_active = False
    right_click_active = False

    print("Hand Gesture Mouse Controller")
    print("Show your hand to the camera.")
    print("Press Q to quit.")

    while True:
        success, frame = camera.read()

        if not success:
            print("ERROR: Could not read webcam frame.")
            break

        # Mirror webcam
        frame = cv2.flip(frame, 1)

        # Detect hand
        frame, landmarks = tracker.process_frame(frame)

        # Detect gesture
        gesture = gesture_detector.detect(landmarks)

        # --------------------------------
        # MOUSE CONTROL
        # --------------------------------
        if landmarks:

            # ==============================
            # MOVE CURSOR
            # ==============================
            if gesture == "MOVE":

                index_x, index_y = landmarks[8]

                camera_width = frame.shape[1]
                camera_height = frame.shape[0]

                target_x = int(
                    index_x / camera_width * screen_width
                )

                target_y = int(
                    index_y / camera_height * screen_height
                )

                # Smooth movement
                screen_x = int(
                    previous_screen_x
                    + (target_x - previous_screen_x) * smooth_factor
                )

                screen_y = int(
                    previous_screen_y
                    + (target_y - previous_screen_y) * smooth_factor
                )

                pyautogui.moveTo(screen_x, screen_y)

                previous_screen_x = screen_x
                previous_screen_y = screen_y

            # ==============================
            # LEFT CLICK
            # ==============================
            elif gesture == "CLICK":

                if not left_click_active:
                    pyautogui.click()
                    left_click_active = True

            else:
                left_click_active = False

            # ==============================
            # RIGHT CLICK
            # ==============================
            if gesture == "RIGHT CLICK":

                if not right_click_active:
                    pyautogui.rightClick()
                    right_click_active = True

            else:
                right_click_active = False

            # ==============================
            # SCROLL UP
            # ==============================
            if gesture == "SCROLL UP":
                pyautogui.scroll(2)

            # ==============================
            # SCROLL DOWN
            # ==============================
            elif gesture == "SCROLL DOWN":
                pyautogui.scroll(-2)

        else:
            left_click_active = False
            right_click_active = False

        # --------------------------------
        # DISPLAY STATUS
        # --------------------------------
        if landmarks:

            cv2.putText(
                frame,
                "HAND DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            # Wrist marker
            wrist_x, wrist_y = landmarks[0]

            cv2.circle(
                frame,
                (wrist_x, wrist_y),
                12,
                (0, 0, 255),
                -1,
            )

        else:

            cv2.putText(
                frame,
                "NO HAND",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )

        # Gesture text
        cv2.putText(
            frame,
            f"Gesture: {gesture}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 0),
            2,
        )

        # Camera window
        cv2.imshow(
            "Hand Gesture Mouse Controller",
            frame,
        )

        # Quit with Q
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q"):
            break

    # Cleanup
    tracker.close()
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()