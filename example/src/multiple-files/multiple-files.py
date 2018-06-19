# 
# This is application demonstrates how you can use cvui when your project has
# multiple files that use cvui.
# 
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

# Import the two dummy external files
from Class1 import Class1
from Class2 import Class2

WINDOW_NAME = 'CVUI Multiple files'

def main():
	frame = np.zeros((300, 500, 3), np.uint8)

	c1 = Class1()
	c2 = Class2()

	# Init cvui and tell it to create a OpenCV window, i.e. cv2.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		c1.renderInfo(frame)
		c2.renderMessage(frame)

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
