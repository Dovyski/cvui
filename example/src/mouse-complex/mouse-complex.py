#
# This is application uses the mouse API to dynamically create a ROI
# for image visualization.
# 
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Mouse - ROI interaction'
ROI_WINDOW	= 'ROI'

def main():
	lena = cv2.imread('lena.jpg')
	frame = np.zeros(lena.shape, np.uint8)
	anchor = cvui.Point()
	roi = cvui.Rect(0, 0, 0, 0)
	working = False

	# Init cvui and tell it to create a OpenCV window, i.e. cv.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with Lena's image
		frame[:] = lena[:]

		# Show the coordinates of the mouse pointer on the screen
		cvui.text(frame, 10, 10, 'Click (any) mouse button and drag the pointer around to select a ROI.')

		# The function 'bool cvui.mouse(int query)' allows you to query the mouse for events.
		# E.g. cvui.mouse(cvui.DOWN)
		#
		# Available queries:
		#	- cvui.DOWN: any mouse button was pressed. cvui.mouse() returns true for single frame only.
		#	- cvui.UP: any mouse button was released. cvui.mouse() returns true for single frame only.
		#	- cvui.CLICK: any mouse button was clicked (went down then up, no matter the amount of frames in between). cvui.mouse() returns true for single frame only.
		#	- cvui.IS_DOWN: any mouse button is currently pressed. cvui.mouse() returns true for as long as the button is down/pressed.

		# Did any mouse button go down?
		if cvui.mouse(cvui.DOWN):
			# Position the anchor at the mouse pointer.
			anchor.x = cvui.mouse().x
			anchor.y = cvui.mouse().y

			# Inform we are working, so the ROI window is not updated every frame
			working = True

		# Is any mouse button down (pressed)?
		if cvui.mouse(cvui.IS_DOWN):
			# Adjust roi dimensions according to mouse pointer
			width = cvui.mouse().x - anchor.x
			height = cvui.mouse().y - anchor.y
			
			roi.x = anchor.x + width if width < 0 else anchor.x
			roi.y = anchor.y + height if height < 0 else anchor.y
			roi.width = abs(width)
			roi.height = abs(height)

			# Show the roi coordinates and size
			cvui.printf(frame, roi.x + 5, roi.y + 5, 0.3, 0xff0000, '(%d,%d)', roi.x, roi.y)
			cvui.printf(frame, cvui.mouse().x + 5, cvui.mouse().y + 5, 0.3, 0xff0000, 'w:%d, h:%d', roi.width, roi.height)

		# Was the mouse clicked (any button went down then up)?
		if cvui.mouse(cvui.UP):
			# We are done working with the ROI.
			working = False

		# Ensure ROI is within bounds
		lenaRows, lenaCols, lenaChannels = lena.shape
		roi.x = 0 if roi.x < 0 else roi.x
		roi.y = 0 if roi.y < 0 else roi.y
		roi.width = roi.width + lena.cols - (roi.x + roi.width) if roi.x + roi.width > lenaCols else roi.width
		roi.height = roi.height + lena.rows - (roi.y + roi.height) if roi.y + roi.height > lenaRows else roi.height

		# Render the roi
		cvui.rect(frame, roi.x, roi.y, roi.width, roi.height, 0xff0000)

		# This function must be called *AFTER* all UI components. It does
		# all the behind the scenes magic to handle mouse clicks, etc.
		cvui.update()

		# Show everything on the screen
		cv2.imshow(WINDOW_NAME, frame)

		# If the ROI is valid, show it.
		if roi.area() > 0 and working == False:
			lenaRoi = lena[roi.y : roi.y + roi.height, roi.x : roi.x + roi.width]
			cv2.imshow(ROI_WINDOW, lenaRoi)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
	main()