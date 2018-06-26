#
# This is a demo application to showcase the image button component.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Image button'

def main():
	frame = np.zeros((300, 600, 3), np.uint8)
	out = cv2.imread('lena-face.jpg', cv2.IMREAD_COLOR)
	down = cv2.imread('lena-face-red.jpg', cv2.IMREAD_COLOR)
	over = cv2.imread('lena-face-gray.jpg', cv2.IMREAD_COLOR)

	# Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# Render an image-based button. You can provide images
		# to be used to render the button when the mouse cursor is
		# outside, over or down the button area.
		if cvui.button(frame, 200, 80, out, over, down):
			print('Image button clicked!')

		cvui.text(frame, 150, 200, 'This image behaves as a button')

		# Render a regular button.
		if cvui.button(frame, 360, 80, 'Button'):
			print('Regular button clicked!')

		# This function must be called *AFTER* all UI components. It does
		# all the behind the scenes magic to handle mouse clicks, etc.
		cvui.update()

		# Show everything on the screen
		cv2.imshow(WINDOW_NAME, frame)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
    main()
