#
# This is a demo application to showcase the input component. 
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
    
	input = ["text"]

	while (True):
		frame[:] = (49, 52, 49)

		# An input component requires a position (x and y), a width, a unique name
        # and a value (which will automatically change according to user interaction).
        # If you use the same name for different inputs, their focus will not work properly.
		cvui.input(frame, 40, 40, 100, "myInput", input)

		cvui.text(frame, 160, 50, "Click the input to edit.")

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
