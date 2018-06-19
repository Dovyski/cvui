#
# This is a demo application to showcase the use of trackbars and columns.
#
# Author:
#	Pascal Thomet
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

WINDOW_NAME	= 'Trackbar and columns'

def main():
	intValue = [30]
	ucharValue = [30]
	charValue = [30]
	floatValue = [12.]
	doubleValue1 = [15.]
	doubleValue2 = [10.3]
	doubleValue3 = [2.25]
	frame = np.zeros((650, 450, 3), np.uint8)

	# Size of trackbars
	width = 400

	# Init cvui and tell it to use a value of 20 for cv2.waitKey()
	# because we want to enable keyboard shortcut for
	# all components, e.g. button with label '&Quit'.
	# If cvui has a value for waitKey, it will call
	# waitKey() automatically for us within cvui.update().
	cvui.init(WINDOW_NAME, 20)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		cvui.beginColumn(frame, 20, 20, -1, -1, 6)
		
		cvui.text('int trackbar, no customization')
		cvui.trackbar(width, intValue, 0, 100)
		cvui.space(5)

		cvui.text('uchar trackbar, no customization')
		cvui.trackbar(width, ucharValue, 0, 255)
		cvui.space(5)

		cvui.text('signed char trackbar, no customization')
		cvui.trackbar(width, charValue, -128, 127)
		cvui.space(5)

		cvui.text('float trackbar, no customization')
		cvui.trackbar(width, floatValue, 10., 15.)
		cvui.space(5)

		cvui.text('float trackbar, 4 segments')
		cvui.trackbar(width, doubleValue1, 10., 20., 4)
		cvui.space(5)

		cvui.text('double trackbar, label %.1Lf, TRACKBAR_DISCRETE')
		cvui.trackbar(width, doubleValue2, 10., 10.5, 1, '%.1Lf', cvui.TRACKBAR_DISCRETE, 0.1)
		cvui.space(5)

		cvui.text('double trackbar, label %.2Lf, 2 segments, TRACKBAR_DISCRETE')
		cvui.trackbar(width, doubleValue3, 0., 4., 2, '%.2Lf', cvui.TRACKBAR_DISCRETE, 0.25)
		cvui.space(10)

		# Exit the application if the quit button was pressed.
		# It can be pressed because of a mouse click or because 
		# the user pressed the 'q' key on the keyboard, which is
		# marked as a shortcut in the button label ('&Quit').
		if cvui.button('&Quit'):
			break
		
		cvui.endColumn()

		# Since cvui.init() received a param regarding waitKey,
		# there is no need to call cv.waitKey() anymore. cvui.update()
		# will do it automatically.
		cvui.update()

		cv2.imshow(WINDOW_NAME, frame)

if __name__ == '__main__':
    main()
