import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import os as oss
import traceback

# Initialize video capture and hand detectors
capture = cv2.VideoCapture(0)
if not capture.isOpened():
    print("Error: Unable to access the camera.")
    exit()

hd = HandDetector(maxHands=1)
hd2 = HandDetector(maxHands=1)

# Initialize directory settings
count = len(oss.listdir("AtoZ_3.1\\A\\"))
c_dir = 'A'

offset = 15
step = 1
flag = False
suv = 0

# Create a blank white image for skeleton drawing
white = np.ones((400, 400), np.uint8) * 255  # This is your canvas
cv2.imwrite("white.jpg", white)


while True:
    try:
        # Capture the frame
        _, frame = capture.read()
        frame = cv2.flip(frame, 1)  # Mirror the frame for ease of interaction

        # Create the skeleton canvas as a copy of the white canvas
        skeleton1 = np.copy(white)  # Ensure skeleton1 is always defined

        # Detect hands in the frame
        hands = hd.findHands(frame, draw=False, flipType=True)
        print("Hands detected:", hands)

        # Load the white canvas (if needed) or reuse the one initialized before
        white = np.ones((400, 400), np.uint8) * 255  # Reset the white canvas

        if hands:
            hand = hands[0]
            if isinstance(hand, dict) and 'bbox' in hand:
                x, y, w, h = hand['bbox']
                image = np.array(frame[y - offset:y + h + offset, x - offset:x + w + offset])

                # Check if the cropped image is not empty
                if image.size > 0:
                    # Detect landmarks in the cropped hand image
                    handz, imz = hd2.findHands(image, draw=True, flipType=True)

                    if handz:
                        hand = handz[0]
                        pts = hand['lmList']  # List of landmarks: each item is [x, y, z]

                        # Debug: Print the detected landmarks to check the x, y, z values
                        print("Detected Landmarks:", pts)

                        # Calculate the offset to center the hand on the canvas (400x400)
                        os = ((400 - w) // 2) - 15  # X offset
                        os1 = ((400 - h) // 2) - 15  # Y offset

                        # Debug: Print the offsets
                        print(f"Offsets: os={os}, os1={os1}")

                                                # Loop through landmarks and draw lines between connected points
                                                # Ensure landmarks are valid
                        if len(pts) == 21:  # Check that there are 21 landmarks
                            for i, pt in enumerate(pts):
                                print(f"Landmark {i}: x={pt[0]}, y={pt[1]}, z={pt[2]}")

                            # Calculate offsets for centering on 400x400 canvas
                            os = (400 - w) // 2 - 15
                            os1 = (400 - h) // 2 - 15

                            # Print offsets for debugging
                            print(f"os: {os}, os1: {os1}")

                            # Draw the lines between landmarks
                            for t in range(0, 4):
                                cv2.line(white, (pts[t][0] + os, pts[t][1] + os1),
                                        (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)

                            for t in range(5, 8):
                                cv2.line(white, (pts[t][0] + os, pts[t][1] + os1),
                                        (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)

                            for t in range(9, 12):
                                cv2.line(white, (pts[t][0] + os, pts[t][1] + os1),
                                        (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)

                            for t in range(13, 16):
                                cv2.line(white, (pts[t][0] + os, pts[t][1] + os1),
                                        (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)

                            for t in range(17, 20):
                                cv2.line(white, (pts[t][0] + os, pts[t][1] + os1),
                                        (pts[t + 1][0] + os, pts[t + 1][1] + os1), (0, 255, 0), 3)

                            # Draw the connections between key points
                            cv2.line(white, (pts[5][0] + os, pts[5][1] + os1),
                                    (pts[9][0] + os, pts[9][1] + os1), (0, 255, 0), 3)
                            cv2.line(white, (pts[9][0] + os, pts[9][1] + os1),
                                    (pts[13][0] + os, pts[13][1] + os1), (0, 255, 0), 3)
                            cv2.line(white, (pts[13][0] + os, pts[13][1] + os1),
                                    (pts[17][0] + os, pts[17][1] + os1), (0, 255, 0), 3)
                            cv2.line(white, (pts[0][0] + os, pts[0][1] + os1),
                                    (pts[5][0] + os, pts[5][1] + os1), (0, 255, 0), 3)
                            cv2.line(white, (pts[0][0] + os, pts[0][1] + os1),
                                    (pts[17][0] + os, pts[17][1] + os1), (0, 255, 0), 3)

                            # Draw circles on the landmarks
                            for i in range(21):
                                cv2.circle(white, (pts[i][0] + os, pts[i][1] + os1), 2, (0, 0, 255), 1)

                            # Display the result
                            cv2.imshow("Skeleton", white)
                        else:
                            print("Invalid number of landmarks!")

                        # After drawing the skeleton, copy the result to skeleton1
                        skeleton1 = np.array(white)
                        cv2.imshow("Skeleton", skeleton1)
                # Display the frame with count info
        frame = cv2.putText(frame, "dir=" + str(c_dir) + "  count=" + str(count), (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 1, cv2.LINE_AA)
        cv2.imshow("frame", frame)

        interrupt = cv2.waitKey(1)
        if interrupt & 0xFF == 27:  # esc key
            break

        # Change directory on 'n' key press
        if interrupt & 0xFF == ord('n'):
            c_dir = chr(ord(c_dir) + 1)
            if ord(c_dir) == ord('Z') + 1:
                c_dir = 'A'
            count = len(oss.listdir(f"AtoZ_3.1\\{c_dir}\\"))

        # Toggle frame saving with 'a' key
        if interrupt & 0xFF == ord('a'):
            flag = not flag
            suv = 0 if flag else suv

        # Save frames at intervals when flag is true
        if flag and step % 3 == 0:
            cv2.imwrite(f"AtoZ_3.1\\{c_dir}\\{count}.jpg", skeleton1)
            count += 1
            suv += 1

        step += 1  # Increment step counter

    except Exception as e:
        print("Error:", traceback.format_exc())

# Clean up
capture.release()
cv2.destroyAllWindows()
