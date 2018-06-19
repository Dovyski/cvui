"""
This demo shows how you can use cvui in an application that uses
more than one OpenCV window. When using cvui with multiple OpenCV
windows, you must call cvui component calls between cvui.contex(NAME)
and cvui.update(NAME), where NAME is the name of the window.
That way, cviu knows which window you are using (NAME in this case),
so it can track mouse events, for instance.

E.g.

  # Code for window 'window1'.
  cvui.context('window1')
  cviu.text(frame, ...)
  cviu.button(frame, ...)
  cviu.update('window1')

  # somewhere else, code for 'window2'
  cvui.context('window2')
  cviu.printf(frame, ...)
  cviu.printf(frame, ...)
  cviu.update('window2')

  # Show everything in a window
  cv2.imshow(frame)

Pay attention to the pair cvui.context(NAME)/cviu.update(NAME), which
encloses the component calls for that window. You need such pair for
each window of your application.

After calling cvui.update(), you can show the result in a window using cv2.imshow().
If you want to save some typing, you can use cvui.imshow(), which calls cvui.update()
for you and then shows the frame in a window.

E.g.

  # Code for window 'window1'.
  cvui.context('window1')
  cviu.text(frame, ...)
  cviu.button(frame, ...)
  cviu.imshow('window1')

  # somewhere else, code for 'window2'
  cvui.context('window2')
  cviu.printf(frame, ...)
  cviu.printf(frame, ...)
  cviu.imshow('window2')

In that case, you don't have to bother calling cvui.update() yourself, since
cvui.imshow() will do it for you.

Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
"""

import numpy as np
import cv2
import cvui

WINDOW1_NAME = 'Window 1'
WINDOW2_NAME = 'Windows 2'
WINDOW3_NAME = 'Windows 3'
WINDOW4_NAME = 'Windows 4'

# Update a window using cvui functions, then show it using cv2.imshow().
def window(name):
	# Create a frame for this window and fill it with a nice color
	frame = np.zeros((200, 500, 3), np.uint8)
	frame[:] = (49, 52, 49)

	# Inform cvui that the components to be rendered from now one belong to
	# a window in particular.
	#
	# If you don't inform that, cvui will assume the components belong to
	# the default window (informed in cvui.init()). In that case, the
	# interactions with all other windows being used will not work.
	cvui.context(name)

	# Show info regarding the window
	cvui.printf(frame, 110, 50, '%s - click the button', name)

	# Buttons return true if they are clicked
	if cvui.button(frame, 110, 90, 'Button'):
		cvui.printf(frame, 200, 95, 'Button clicked!')
		print('Button clicked on: ', name)

	# Tell cvui to update its internal structures regarding a particular window.
	#
	# If cvui is being used in multiple windows, you need to enclose all component
	# calls between the pair cvui.context(NAME)/cvui.update(NAME), where NAME is
	# the name of the window being worked on.
	cvui.update(name)

	# Show the content of this window on the screen
	cvui.imshow(name, frame)

# Update and show a window in a single call using cvui.imshow().
def compact(name):
	# Create a frame for this window and fill it with a nice color
	frame = np.zeros((200, 500, 3), np.uint8)
	frame[:] = (49, 52, 49)

	# Inform cvui that the components to be rendered from now one belong to
	# a window in particular.
	#
	# If you don't inform that, cvui will assume the components belong to
	# the default window (informed in cvui.init()). In that case, the
	# interactions with all other windows being used will not work.
	cvui.context(name)

	cvui.printf(frame, 110, 50, '%s - click the button', name)
	if cvui.button(frame, 110, 90, 'Button'):
		cvui.printf(frame, 200, 95, 'Button clicked!')
		print('Button clicked on: ', name)

	# Tell cvui to update its internal structures regarding a particular window
	# then show it. Below we are using cvui.imshow(), which is cvui's version of
	# the existing cv2.imshow(). They behave exactly the same, the only difference
	# is that cvui.imshow() will automatically call cvui.update(name) for you.
	cvui.imshow(name, frame)

def main():
	# Init cvui. If you don't tell otherwise, cvui will create the required OpenCV
	# windows based on the list of names you provided.
	windows = [WINDOW1_NAME, WINDOW2_NAME, WINDOW3_NAME, WINDOW4_NAME]
	cvui.init(windows, 4)

	while (True):
		# The functions below will update a window and show them using cv2.imshow().
		# In that case, you must call the pair cvui.context(NAME)/cvui.update(NAME)
		# to render components and update the window.
		window(WINDOW1_NAME)
		window(WINDOW2_NAME)
		window(WINDOW3_NAME)
		
		# The function below will do the same as the funcitons above, however it will
		# use cvui.imshow() (cvui's version of cv2.imshow()), which will automatically
		# call cvui.update() for us.
		compact(WINDOW4_NAME)

		# Check if ESC key was pressed
		if cv2.waitKey(20) == 27:
			break

if __name__ == '__main__':
	main()