#
# This is a demo application to showcase the UI components of cvui.
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

WINDOW_NAME	= 'CVUI Test'

def main():
	lena = cv2.imread('lena.jpg', cv2.IMREAD_COLOR)
	frame = np.zeros(lena.shape, np.uint8)
	doubleBuffer = np.zeros(lena.shape, np.uint8)
	trackbarWidth = 130

	# Adjustments values for RGB and HSV
	rgb = [[1.], [1.], [1]]
	hsv = [[1.], [1.], [1]]

	# Copy the loaded image to the buffer
	doubleBuffer[:] = lena[:]

	# Init cvui and tell it to use a value of 20 for cv2.waitKey()
	# because we want to enable keyboard shortcut for
	# all components, e.g. button with label '&Quit'.
	# If cvui has a value for waitKey, it will call
	# waitKey() automatically for us within cvui.update().
	cvui.init(WINDOW_NAME, 20)

	while (True):
		frame[:] = doubleBuffer[:]
		frameRows,frameCols,frameChannels = frame.shape

		# Exit the application if the quit button was pressed.
		# It can be pressed because of a mouse click or because 
		# the user pressed the 'q' key on the keyboard, which is
		# marked as a shortcut in the button label ('&Quit').
		if cvui.button(frame, frameCols - 100, frameRows - 30, '&Quit'):
			break

		# RGB HUD
		cvui.window(frame, 20, 50, 180, 240, 'RGB adjust')

		# Within the cvui.beginColumns() and cvui.endColumn(),
		# all elements will be automatically positioned by cvui.
		# In a columns, all added elements are vertically placed,
		# one under the other (from top to bottom).
		#
		# Notice that all component calls within the begin/end block
		# below DO NOT have (x,y) coordinates.
		#
		# Let's create a row at position (35,80) with automatic
		# width and height, and a padding of 10
		cvui.beginColumn(frame, 35, 80, -1, -1, 10)
		rgbModified = False

		# Trackbar accept a pointer to a variable that controls their value
		# They return true upon edition
		if cvui.trackbar(trackbarWidth, rgb[0], 0., 2., 2, '%3.02Lf'):
			rgbModified = True

		if cvui.trackbar(trackbarWidth, rgb[1], 0., 2., 2, '%3.02Lf'):
			rgbModified = True

		if cvui.trackbar(trackbarWidth, rgb[2], 0., 2., 2, '%3.02Lf'):
			rgbModified = True
			
		cvui.space(2)
		cvui.printf(0.35, 0xcccccc, '   RGB: %3.02lf,%3.02lf,%3.02lf', rgb[0][0], rgb[1][0], rgb[2][0])

		if (rgbModified):
			b,g,r = cv2.split(lena)
			b = b * rgb[2][0]
			g = g * rgb[1][0]
			r = r * rgb[0][0]
			cv2.merge((b,g,r), doubleBuffer)
		cvui.endColumn()

		# HSV
		lenaRows,lenaCols,lenaChannels = lena.shape
		cvui.window(frame, lenaCols - 200, 50, 180, 240, 'HSV adjust')
		cvui.beginColumn(frame, lenaCols - 180, 80, -1, -1, 10)
		hsvModified = False
			
		if cvui.trackbar(trackbarWidth, hsv[0], 0., 2., 2, '%3.02Lf'):
			hsvModified = True

		if cvui.trackbar(trackbarWidth, hsv[1], 0., 2., 2, '%3.02Lf'):
			hsvModified = True

		if cvui.trackbar(trackbarWidth, hsv[2], 0., 2., 2, '%3.02Lf'):
			hsvModified = True

		cvui.space(2)
		cvui.printf(0.35, 0xcccccc, '   HSV: %3.02lf,%3.02lf,%3.02lf', hsv[0][0], hsv[1][0], hsv[2][0])

		if hsvModified:
			hsvMat = cv2.cvtColor(lena, cv2.COLOR_BGR2HSV)
			h,s,v = cv2.split(hsvMat)
			h = h * hsv[0][0]
			s = s * hsv[1][0]
			v = v * hsv[2][0]
			cv2.merge((h,s,v), hsvMat)
			doubleBuffer = cv2.cvtColor(hsvMat, cv2.COLOR_HSV2BGR)

		cvui.endColumn()

		# Display the lib version at the bottom of the screen
		cvui.printf(frame, frameCols - 300, frameRows - 20, 0.4, 0xCECECE, 'cvui v.%s', cvui.VERSION)

		# This function must be called *AFTER* all UI components. It does
		# all the behind the scenes magic to handle mouse clicks, etc.
		#
		# Since cvui.init() received a param regarding waitKey,
		# there is no need to call cv2.waitKey() anymore. cvui.update()
		# will do it automatically.
		cvui.update()

		# Show everything on the screen
		cv2.imshow(WINDOW_NAME, frame)

if __name__ == '__main__':
    main()
