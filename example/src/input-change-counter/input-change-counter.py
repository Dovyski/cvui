#
# This is a demo application to showcase the input component. 
# 
# Copyright (c) 2022 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
# 
import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Input change counter'

def main():
	frame = np.zeros((150, 650, 3), np.uint8)

	# Init cvui and tell it to use a value of 20 for cv2.waitKey()
	# because we want to enable keyboard shortcut for
	# all components, e.g. button with label "&Quit".
	# If cvui has a value for waitKey, it will call
	# waitKey() automatically for us within cvui.update().
	cvui.init(WINDOW_NAME, 20)
    
	input = ["123"]
	count = [0]

	while (True):
		frame[:] = (49, 52, 49)

		# Input component will return an integer value representing
		# they key that was pressed.
		key = cvui.input(frame, 40, 40, 100, "myInput", input)

		cvui.printf(frame, 160, 50, "Click the input, type a number then press enter")

        # The contants defined as cvui.KEY_* can be used to identify pressed keys.
        # You can use them to detect special keys as cvui.KEY_HOME and cvui.KEY_END.
		if key == cvui.KEY_ENTER:
			inputValue = int(input[0])
			count = [inputValue]

		cvui.counter(frame, 500, 45, count)			

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
