# Restricted Area Entry Detection Project
import cv2
import winsound
import keyboard
import threading
import time
backSub = cv2.createBackgroundSubtractorMOG2(
    history=500,
    varThreshold=25,
    detectShadows=False
)
alarm_running = False
alarm_enabled = True
motion_latched = False
def alarm():
    global alarm_running
    while alarm_running:
        winsound.Beep(1000, 1000)
cap = cv2.VideoCapture(0)
start_time = time.time()
while True:
    success, frame = cap.read()
    if not success:
        break
    if keyboard.is_pressed('s'):
        alarm_enabled = not alarm_enabled
        # Stop any running alarm immediately
        if not alarm_enabled:
            alarm_running = False
        time.sleep(0.3)
    if keyboard.is_pressed('enter'):
        alarm_running = False
        time.sleep(0.3)
    fgMask = backSub.apply(frame)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    fgMask = cv2.morphologyEx(fgMask, cv2.MORPH_OPEN, kernel)
    fgMask = cv2.dilate(fgMask, kernel, iterations=2)
    contours, _ = cv2.findContours(
        fgMask,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )
    motionDetected = False
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 1500:
            motionDetected = True
            x, y, w, h = cv2.boundingRect(cnt)
            cv2.rectangle(
                frame,
                (x, y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )
    if (time.time() - start_time) > 3:
        if motionDetected:
            cv2.putText(
                frame,
                "MOTION DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )
            if alarm_enabled and not motion_latched:
                motion_latched = True
                if not alarm_running:
                    alarm_running = True
                    threading.Thread(
                        target=alarm,
                        daemon=True
                    ).start()
        else:
            motion_latched = False
    if alarm_enabled:
        cv2.putText(
            frame,
            "ALARM : ON (Press s to OFF)",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2
        )
    else:
        cv2.putText(
            frame,
            "ALARM : OFF (Press s to ON)",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 0, 255),
            2
        )
    cv2.imshow("Motion Detection", frame)
    # cv2.imshow("Motion Mask", fgMask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
alarm_running = False
cap.release()
cv2.destroyAllWindows()



# The Restricted Area Entry Detection System uses a webcam to monitor a restricted area.
# It detects any movement in the area and draws a box around the moving object.
# If movement is detected, the system sounds an alarm to warn about possible unauthorized entry.
