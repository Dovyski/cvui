#
# This application showcases how the window component of cvui can be
# enhanced, i.e. make it movable anb minimizable.
# 
# Authors:
#	ShengYu - https://github.com/shengyu7697
#	Amaury Breheret - https://github.com/abreheret
# 
# Contributions:
#	Fernando Bevilacqua <dovyski@gmail.com>
# 
# Copyright (c) 2018 Authors and Contributors
# Code licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

# Include the enhanced cvui window component, i.e. EnhancedWindow.py
from EnhancedWindow import EnhancedWindow

WINDOW_NAME	= 'CVUI Enhanced Window Component'

def main():
	frame = np.zeros((600, 800, 3), np.uint8)
	value = [50]
	
	settings = EnhancedWindow(20, 80, 200, 120, 'Settings')
	info = EnhancedWindow(250, 80, 330, 60, 'Info')

	# Init cvui and tell it to create a OpenCV window, i.e. cv2.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# Place some instructions on the screen regarding the
		# settings window
		cvui.text(frame, 20, 20, 'The Settings and the Info windows below are movable and minimizable.')
		cvui.text(frame, 20, 40, 'Click and drag any window\'s title bar to move it around.')

		# Render a movable and minimizable settings window using
		# the EnhancedWindow class.
		settings.begin(frame)
		if settings.isMinimized() == False:
			cvui.text('Adjust something')
			cvui.space(10) # add 10px of space between UI components
			cvui.trackbar(settings.width() - 20, value, 5, 150)
		settings.end()

		# Render a movable and minimizable settings window using
		# the EnhancedWindow class.
		info.begin(frame)
		if info.isMinimized() == False:
			cvui.text('Moving and minimizable windows are awesome!')
		info.end()

		# Update all cvui internal stuff, e.g. handle mouse clicks, and show
		# everything on the screen.
		cvui.imshow(WINDOW_NAME, frame)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
    main()
