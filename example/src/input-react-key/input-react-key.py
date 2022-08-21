#
# This is a demo application to showcase how to react to a particular
# key when it is pressed in an input component, e.g. enter.
# 
# Copyright (c) 2022 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
# 
import numpy as np
import cv2
import cvui

WINDOW_NAME	= 'Input react to key'

def main():
	frame = np.zeros((150, 650, 3), np.uint8)

	# Init cvui and tell it to use a value of 20 for cv2.waitKey()
	# because we want to enable keyboard shortcut for
	# all components, e.g. button with label "&Quit".
	# If cvui has a value for waitKey, it will call
	# waitKey() automatically for us within cvui.update().
	cvui.init(WINDOW_NAME, 20)
    
	input = ["text"]

	while (True):
		frame[:] = (49, 52, 49)

		# The value retorned by cvui::input() is an int that identifies a keyboard key.
        # The contants defined as cvui::KEY_* can be used to identify those keys.
        # You can use them to detect special keys as cvui::KEY_HOME and cvui::KEY_END.
		key = cvui.input(frame, 40, 40, 100, "myInput", input)

		cvui.printf(frame, 160, 50, "Click the input to edit. After press enter")

		# The contants defined as cvui.KEY_* can be used to identify pressed keys.
        # You can use them to detect special keys as cvui.KEY_HOME and cvui.KEY_END.
		if key == cvui.KEY_ENTER:
			print("Enter pressed")

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
