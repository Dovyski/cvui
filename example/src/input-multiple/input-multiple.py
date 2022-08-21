#
# This is a demo application to showcase how to use multiple inputs
# at the same time
# 
# Copyright (c) 2022 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
# 
import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Input multiple'

def main():
	frame = np.zeros((150, 650, 3), np.uint8)

	# Init cvui and tell it to use a value of 20 for cv2.waitKey()
	# because we want to enable keyboard shortcut for
	# all components, e.g. button with label "&Quit".
	# If cvui has a value for waitKey, it will call
	# waitKey() automatically for us within cvui.update().
	cvui.init(WINDOW_NAME, 20)
    
	input1 = ["text1"]
	input2 = ["text2"]

	while (True):
		frame[:] = (49, 52, 49)

		# Each input must have a unique name to ensure its focus behavior works.
		# In the inputs below, the first one is uniquely named `myInput1` and the
		# second one is uniquely named `myInput2`.
		cvui.input(frame, 40, 40, 100, "myInput1", input1);
		cvui.input(frame, 40, 80, 100, "myInput2", input2);

		cvui.text(frame, 160, 50, "Click any input to edit.");

		# Exit the application if the quit button was pressed.
		# It can be pressed because of a mouse click or because 
		# the user pressed the "q" key on the keyboard, which is
		# marked as a shortcut in the button label ("&Quit").
		if cvui.button(frame, 300, 100, "&Quit"):
			break

		# Since cvui.init() received a param regarding waitKey,
		# there is no need to call cv2.waitKey() anymore. cvui.update()
		# will do it automatically.
		cvui.update()
		
		cv2.imshow(WINDOW_NAME, frame)

if __name__ == '__main__':
    main()
