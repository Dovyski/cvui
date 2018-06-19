#
# This is application uses the fine details of the mouse API to dynamically
# create ROIs for image visualization based on different mouse buttons.
# 
# This demo is very similiar to 'mouse-complex', except that it handles 3 ROIs,
# one for each mouse button.
# 
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Mouse complex buttons- ROI interaction'

def main():
	lena = cv2.imread('lena.jpg')
	frame = np.zeros(lena.shape, np.uint8)
	anchors = [cvui.Point() for i in range(3)]   # one anchor for each mouse button
	rois = [cvui.Rect() for i in range(3)]       # one ROI for each mouse button
	colors = [0xff0000, 0x00ff00, 0x0000ff]

	# Init cvui and tell it to create a OpenCV window, i.e. cv.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with Lena's image
		frame[:] = lena[:]

		# Show the coordinates of the mouse pointer on the screen
		cvui.text(frame, 10, 10, 'Click (any) mouse button then drag the pointer around to select a ROI.')
		cvui.text(frame, 10, 25, 'Use different mouse buttons (right, middle and left) to select different ROIs.')

		# Iterate all mouse buttons (left, middle  and right button)
		button = cvui.LEFT_BUTTON
		while button <= cvui.RIGHT_BUTTON:
			# Get the anchor, ROI and color associated with the mouse button
			anchor = anchors[button]
			roi = rois[button]
			color = colors[button]

			# The function 'bool cvui.mouse(int button, int query)' allows you to query a particular mouse button for events.
			# E.g. cvui.mouse(cvui.RIGHT_BUTTON, cvui.DOWN)
			#
			# Available queries:
			#	- cvui.DOWN: mouse button was pressed. cvui.mouse() returns true for single frame only.
			#	- cvui.UP: mouse button was released. cvui.mouse() returns true for single frame only.
			#	- cvui.CLICK: mouse button was clicked (went down then up, no matter the amount of frames in between). cvui.mouse() returns true for single frame only.
			#	- cvui.IS_DOWN: mouse button is currently pressed. cvui.mouse() returns true for as long as the button is down/pressed.

			# Did the mouse button go down?
			if cvui.mouse(button, cvui.DOWN):
				# Position the anchor at the mouse pointer.
				anchor.x = cvui.mouse().x
				anchor.y = cvui.mouse().y

			# Is any mouse button down (pressed)?
			if cvui.mouse(button, cvui.IS_DOWN):
				# Adjust roi dimensions according to mouse pointer
				width = cvui.mouse().x - anchor.x
				height = cvui.mouse().y - anchor.y

				roi.x = anchor.x + width if width < 0 else anchor.x
				roi.y = anchor.y + height if height < 0 else anchor.y
				roi.width = abs(width)
				roi.height = abs(height)

				# Show the roi coordinates and size
				cvui.printf(frame, roi.x + 5, roi.y + 5, 0.3, color, '(%d,%d)', roi.x, roi.y)
				cvui.printf(frame, cvui.mouse().x + 5, cvui.mouse().y + 5, 0.3, color, 'w:%d, h:%d', roi.width, roi.height)

			# Ensure ROI is within bounds
			lenaRows, lenaCols, lenaChannels = lena.shape
			roi.x = 0 if roi.x < 0 else roi.x
			roi.y = 0 if roi.y < 0 else roi.y
			roi.width = roi.width + lenaCols - (roi.x + roi.width) if roi.x + roi.width > lenaCols else roi.width
			roi.height = roi.height + lenaRows - (roi.y + roi.height) if roi.y + roi.height > lenaRows else roi.height

			# If the ROI is valid, render it in the frame and show in a window.
			if roi.area() > 0:
				cvui.rect(frame, roi.x, roi.y, roi.width, roi.height, color)
				cvui.printf(frame, roi.x + 5, roi.y - 10, 0.3, color, 'ROI %d', button)

				lenaRoi = lena[roi.y : roi.y + roi.height, roi.x : roi.x + roi.width]
				cv2.imshow('ROI button' + str(button), lenaRoi)

			button += 1

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