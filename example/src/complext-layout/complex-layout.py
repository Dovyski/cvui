#
# This application showcases how UI components can be placed
# to create a more complex layout. The position of all components
# is determined by a (x,y) pair prodived by the developer.
# 
# Take a look at the "row-column" application to see how to use
# automatic positioning by leveraging the begin*()/end*() API.
# 
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Complex layout'

def group(frame, x, y, width, height):
	padding = 5
	w = (width - padding) / 4
	h = (height - 15 - padding) / 2
	pos = cvui.Point(x + padding, y + 5)

	cvui.text(frame, pos.x, pos.y, 'Group title')
	pos.y += 15

	cvui.window(frame, pos.x, pos.y, width - padding * 2, h - padding, 'Something')
	cvui.rect(frame, pos.x + 2, pos.y + 20, width - padding * 2 - 5, h - padding - 20, 0xff0000)
	pos.y += h

	cvui.window(frame, pos.x, pos.y, w / 3 - padding, h, 'Some')
	cvui.text(frame, pos.x + 25, pos.y + 60, '65', 1.1)
	pos.x += w / 3

	cvui.window(frame, pos.x, pos.y, w / 3 - padding, h, 'Info')
	cvui.text(frame, pos.x + 25, pos.y + 60, '30', 1.1)
	pos.x += w / 3

	cvui.window(frame, pos.x, pos.y, w / 3 - padding, h, 'Here')
	cvui.text(frame, pos.x + 25, pos.y + 60, '70', 1.1)
	pos.x += w / 3

	cvui.window(frame, pos.x, pos.y, w - padding, h, 'And')
	cvui.rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000)
	pos.x += w

	cvui.window(frame, pos.x, pos.y, w - padding, h, 'Here')
	cvui.rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000)
	pos.x += w

	cvui.window(frame, pos.x, pos.y, w - padding, h, 'More info')
	cvui.rect(frame, pos.x + 2, pos.y + 22, w - padding - 5, h - padding - 20, 0xff0000)
	pos.x += w

def main():
	height = 220
	spacing = 10
	frame = np.zeros((height * 3, 1300, 3), np.uint8)

	# Init cvui and tell it to create a OpenCV window, i.e. cv2.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		rows, cols, channels = frame.shape

		# Render three groups of components.
		group(frame, 0, 0, cols, height - spacing)
		group(frame, 0, height, cols, height - spacing)
		group(frame, 0, height * 2, cols, height - spacing)

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
