#
# This is a demo application to showcase how the input component can be used
# with different font sizes (font scale) and different width.
#
# Copyright (c) 2022 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
# 
import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Simple input'

def main():
	frame = np.zeros((300, 600, 3), np.uint8)

	# Init cvui and tell it to use a value of 20 for cv2.waitKey()
	# because we want to enable keyboard shortcut for
	# all components, e.g. button with label "&Quit".
	# If cvui has a value for waitKey, it will call
	# waitKey() automatically for us within cvui.update().
	cvui.init(WINDOW_NAME, 20)
    
	input1 = ['text']
	input1 = ['default']
	input2 = ['large width']
	input3 = ['font scale']
	input4 = ['width and font scale']

	while (True):
		frame[:] = (49, 52, 49)

		# Display some input elements with different width and font scale.
		cvui.input(frame, 40, 40, 150, "input1", input1)
		cvui.input(frame, 40, 80, 300, "input2", input2)
		cvui.input(frame, 40, 120, 300, "input3", input3, 0.8)
		cvui.input(frame, 40, 200, 400, "input4", input4, 0.9)

		cvui.text(frame, 400, 50, "Click any input to edit.");

		# Exit the application if the quit button was pressed.
		# It can be pressed because of a mouse click or because 
		# the user pressed the "q" key on the keyboard, which is
		# marked as a shortcut in the button label ("&Quit").
		if cvui.button(frame, 500, 200, "&Quit"):
			break

		# Since cvui.init() received a param regarding waitKey,
		# there is no need to call cv2.waitKey() anymore. cvui.update()
		# will do it automatically.
		cvui.update()
		
		cv2.imshow(WINDOW_NAME, frame)

if __name__ == '__main__':
    main()
