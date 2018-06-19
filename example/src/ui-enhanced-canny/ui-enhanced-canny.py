# 
# This application showcases how the window component of cvui can be
# enhanced, i.e. movable anb minimizable, and used to control the
# application of the Canny edge algorithm to a loaded image.
# 
# This application uses the EnhancedWindow class available in the
# "ui-enhanced-window-component" example.
# 
# Author:
#	Fernando Bevilacqua <dovyski@gmail.com>
# 
# Contributions:
# 	Amaury Breheret - https://github.com/abreheret
# 	ShengYu - https://github.com/shengyu7697
# 
# Copyright (c) 2018 Authors and Contributors
# Code licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

# Include the enhanced cvui window component, i.e. EnhancedWindow.py
from EnhancedWindow import EnhancedWindow

WINDOW_NAME	= 'CVUI Canny Edge'

def main():
	fruits = cv2.imread('fruits.jpg', cv2.IMREAD_COLOR)
	frame = np.zeros(fruits.shape, np.uint8)
	low_threshold = [50]
	high_threshold = [150]
	use_canny = [False]

	# Create a settings window using the EnhancedWindow class.
	settings = EnhancedWindow(10, 50, 270, 180, 'Settings')

	# Init cvui and tell it to create a OpenCV window, i.e. cv2.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Should we apply Canny edge?
		if use_canny[0]:
			# Yes, we should apply it.
			frame = cv2.cvtColor(fruits, cv2.COLOR_BGR2GRAY)
			frame = cv2.Canny(frame, low_threshold[0], high_threshold[0], 3)
			frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
		else: 
			# No, so just copy the original image to the displaying frame.
			frame[:] = fruits[:]

		# Render the settings window and its content, if it is not minimized.
		settings.begin(frame)
		if settings.isMinimized() == False:
			cvui.checkbox('Use Canny Edge', use_canny)
			cvui.trackbar(settings.width() - 20, low_threshold, 5, 150)
			cvui.trackbar(settings.width() - 20, high_threshold, 80, 300)
			cvui.space(20); # add 20px of empty space
			cvui.text('Drag and minimize this settings window', 0.4, 0xff0000)
		settings.end()

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
