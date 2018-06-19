#
# This is an extremely simple demo application to showcase the
# basic structure, features and use of cvui.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Hello World!'

def main():
	frame = np.zeros((200, 500, 3), np.uint8)
	count = 0;

	# Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# Buttons will return true if they were clicked, which makes
		# handling clicks a breeze.
		if (cvui.button(frame, 110, 80, "Hello, world!")):
			# The button was clicked, so let's increment our counter.
			count += 1

		# Sometimes you want to show text that is not that simple, e.g. strings + numbers.
		# You can use cvui::printf for that. It accepts a variable number of parameter, pretty
		# much like printf does.
		# Let's show how many times the button has been clicked.
		cvui.printf(frame, 250, 90, 0.4, 0xff0000, "Button click count: %d", count);

		# Update cvui stuff and show everything on the screen
		cvui.imshow(WINDOW_NAME, frame);

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
    main()
