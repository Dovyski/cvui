#
# This is application shows how to use the headless mode.
#
# Copyright (c) 2022 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#
import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Headless'
ENABLE_HEADLESS	= True

def main():
	frame = np.zeros((300, 600, 3), np.uint8)
	state = [False]

	# Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME, 1, True, ENABLE_HEADLESS)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

        # Show some text on the screen
		cvui.text(frame, 50, 30, 'Hey there!')
		
        # Create a checkbox that will never be clicked. This is still OK in headless mode.
		cvui.checkbox(frame, 10, 50, "A checkbox that will never be clicked in headless mode", state)

        # Update and show everything on the screen
        # This is still OK in headless mode.
		cvui.imshow(WINDOW_NAME, frame)

		# This is still OK in headless mode.
		if ENABLE_HEADLESS or cv2.waitKey(20) == 27:
			break

	cv2.imwrite("headless_frame.png", frame)
	print("Wrote headless_frame.png")

if __name__ == '__main__':
    main()
