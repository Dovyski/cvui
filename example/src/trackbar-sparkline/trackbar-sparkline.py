#
# This is a demo application to showcase columns, trackbars and sparklines.
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

WINDOW_NAME	= 'Trackbar and sparkline'

def main():
	frame = np.zeros((300, 800, 3), np.uint8)
	value = [2.25]
	values = []

	# Init cvui and tell it to create a OpenCV window, i.e. cv.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME, 20)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# In a row, all added elements are
		# horizontally placed, one next the other (from left to right)
		#
		# Within the cvui.beginRow() and cvui.endRow(),
		# all elements will be automatically positioned by cvui.
		#
		# Notice that all component calls within the begin/end block
		# DO NOT have (x,y) coordinates.
		#
		# Let's create a row at position (20,80) with automatic width and height, and a padding of 10
		cvui.beginRow(frame, 20, 80, -1, -1, 10);
		
		# trackbar accepts a pointer to a variable that controls their value.
		# Here we define a double trackbar between 0. and 5.
		if cvui.trackbar(150, value, 0., 5.):
			print('Trackbar was modified, value : ', value[0])
			values.append(value[0])

		if len(values) > 5:
			cvui.text('Your edits on a sparkline ->')
			cvui.sparkline(values, 240, 60)

			if cvui.button('Clear sparkline'):
				values = []
		else:
			cvui.text('<- Move the trackbar')
		
		cvui.endRow();

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
