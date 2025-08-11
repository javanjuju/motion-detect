import numpy as np
import cv2 as cv
import base64
import sys
import socketio

#create a socket io client and connect to a socket io server at localhost:5000
# sio = socketio.Client()
# sio.connect("http://localhost:5000")

cap = cv.VideoCapture(0)
initial_frame = None
frame_count = 0
prev_frame = None
motion_detected = False

# convert frame to base64
def encode_frame(frame):
    """Encode the frame as a JPEG and then convert it to base64"""
    _, buffer = cv.imencode('.jpg', frame)  # Encode frame as JPEG
    jpg_as_text = base64.b64encode(buffer).decode('utf-8')  # Convert to base64
    return jpg_as_text

# gets the difference and the threshold
def subtract_frames(frame1, frame2):
    grayFrame1, grayFrame2 = cv.cvtColor(frame1, cv.COLOR_BGR2GRAY), cv.cvtColor(frame2, cv.COLOR_BGR2GRAY)
    diff = cv.absdiff(grayFrame1, grayFrame2)
    _, threshold = cv.threshold(diff, 100, 255, cv.THRESH_BINARY)
    return diff, threshold

while True:
    ret, frame = cap.read()
    if not ret:
        sys.exit("Failed to initialize video capture")
  
    # Set the first frame as the initial frame. This will act like our static object
    # For optimal results use a white background
    if initial_frame is None:
        initial_frame = frame
  
    diff, threshold = None, None
    if prev_frame is not None and initial_frame is not None:
        diff, threshold = subtract_frames(frame, prev_frame)
        contours, _ = cv.findContours(threshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv.contourArea(contour) > 500:  # Filter out small contours (noise)
                motion_detected = True
                x, y, w, h = cv.boundingRect(contour)
                cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        if motion_detected:
            print(f"Motion Detected")
            base_64_frame = encode_frame(frame)
            # sio.emit('motion-detected', {'image': base_64_frame})
            motion_detected = False  # Reset the motion flag after sending

        # Show frame with contours
        cv.imshow('Motion Detection', frame)

    # Set the previous frame
    if initial_frame is not None:
        prev_frame = frame

    # Exit using q
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()
