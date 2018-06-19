#
# This is a demo application to showcase the trackbar component.
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

WINDOW_NAME	= 'Trackbar'

def main():
	intValue = [30]
	ucharValue = [30]
	charValue = [30]
	floatValue = [12.]
	doubleValue = [45.]
	doubleValue2 = [15.]
	doubleValue3 = [10.3]
	frame = np.zeros((770, 350, 3), np.uint8)

	# The width of all trackbars used in this example.
	width = 300

	# The x position of all trackbars used in this example
	x = 10

	# Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# The trackbar component uses templates to guess the type of its arguments.
		# You have to be very explicit about the type of the value, the min and
		# the max params. For instance, if they are double, use 100.0 instead of 100.
		cvui.text(frame, x, 10, 'double, step 1.0 (default)')
		cvui.trackbar(frame, x, 40, width, doubleValue, 0., 100.)

		cvui.text(frame, x, 120, 'float, step 1.0 (default)')
		cvui.trackbar(frame, x, 150, width, floatValue, 10., 15.)

		# You can specify segments and custom labels. Segments are visual marks in
		# the trackbar scale. Internally the value for the trackbar is stored as
		# long double, so the custom labels must always format long double numbers, no
		# matter the type of the numbers being used for the trackbar. E.g. %.2Lf
		cvui.text(frame, x, 230, 'double, 4 segments, custom label %.2Lf')
		cvui.trackbar(frame, x, 260, width, doubleValue2, 0., 20., 4, '%.2Lf')

		# Again: you have to be very explicit about the value, the min and the max params.
		# Below is a uchar trackbar. Observe the uchar cast for the min, the max and 
		# the step parameters.
		cvui.text(frame, x, 340, 'uchar, custom label %.0Lf')
		cvui.trackbar(frame, x, 370, width, ucharValue, 0, 255, 0, '%.0Lf')

		# You can change the behavior of any tracker by using the options parameter.
		# Options are defined as a bitfield, so you can combine them.
		# E.g.
		#	TRACKBAR_DISCRETE							# value changes are discrete
		#  TRACKBAR_DISCRETE | TRACKBAR_HIDE_LABELS	# discrete changes and no labels
		cvui.text(frame, x, 450, 'double, step 0.1, option TRACKBAR_DISCRETE')
		cvui.trackbar(frame, x, 480, width, doubleValue3, 10., 10.5, 1, '%.1Lf', cvui.TRACKBAR_DISCRETE, 0.1)

		# More customizations using options.
		options = cvui.TRACKBAR_DISCRETE | cvui.TRACKBAR_HIDE_SEGMENT_LABELS
		cvui.text(frame, x, 560, 'int, 3 segments, DISCRETE | HIDE_SEGMENT_LABELS')
		cvui.trackbar(frame, x, 590, width, intValue, 10, 50, 3, '%.0Lf', options, 2)

		# Trackbar using char type.
		cvui.text(frame, x, 670, 'char, 2 segments, custom label %.0Lf')
		cvui.trackbar(frame, x, 700, width, charValue, -128, 127, 2, '%.0Lf')

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
