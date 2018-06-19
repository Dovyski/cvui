#
# This is a demo application to showcase keyboard shortcuts. 
#
# Author:
# 	Pascal Thomet
# 
# Contributions:
# 	Fernando Bevilacqua <dovyski@gmail.com>
# 
# Copyright (c) 2018 Authors and Contributors
# Code licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Button shortcut'

def main():
	frame = np.zeros((150, 650, 3), np.uint8)

	# Init cvui and tell it to use a value of 20 for cv2.waitKey()
	# because we want to enable keyboard shortcut for
	# all components, e.g. button with label "&Quit".
	# If cvui has a value for waitKey, it will call
	# waitKey() automatically for us within cvui.update().
	cvui.init(WINDOW_NAME, 20);

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		cvui.text(frame, 40, 40, 'To exit this app click the button below or press Q (shortcut for the button below).')

		# Exit the application if the quit button was pressed.
		# It can be pressed because of a mouse click or because 
		# the user pressed the "q" key on the keyboard, which is
		# marked as a shortcut in the button label ("&Quit").
		if cvui.button(frame, 300, 80, "&Quit"):
			break

		# Since cvui.init() received a param regarding waitKey,
		# there is no need to call cv.waitKey() anymore. cvui.update()
		# will do it automatically.
		cvui.update()
		
		cv2.imshow(WINDOW_NAME, frame)

if __name__ == '__main__':
    main()
