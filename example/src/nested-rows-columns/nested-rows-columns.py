#
# This application demonstrates the use of begin*()/end*() to
# create nested rows/columns. Check the 'row-column' app to
# understand automatic positioning and to check a simpler
# use of begin*()/end*().
# 
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
# 

import numpy as np
import cv2
import cvui
import random

WINDOW_NAME	= 'Nested rows and columns'

def main():
	frame = np.zeros((600, 800, 3), np.uint8)
	values = []
	checked = [False]
	value = [1.0]

	# Fill the vector with a few random values
	for i in range(0, 20):
		values.append(random.uniform(0., 300.0))

	# Init cvui and tell it to create a OpenCV window, i.e. cv.namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# Define a row at position (10, 50) with width 100 and height 150.
		cvui.beginRow(frame, 10, 50, 100, 150)
		# The components below will be placed one beside the other.
		cvui.text('Row starts')
		cvui.button('here')

		# When a column or row is nested within another, it behaves like
		# an ordinary component with the specified size. In this case,
		# let's create a column with width 100 and height 50. The
		# next component added will behave like it was added after
		# a component with width 100 and heigth 150.
		cvui.beginColumn(100, 150)
		cvui.text('Column 1')
		cvui.button('button1')
		cvui.button('button2')
		cvui.button('button3')
		cvui.text('End of column 1')
		cvui.endColumn()

		# Add two pieces of text
		cvui.text('Hi again,')
		cvui.text('its me!')

		# Start a new column
		cvui.beginColumn(100, 50)
		cvui.text('Column 2')
		cvui.button('button1')
		cvui.button('button2')
		cvui.button('button3')
		cvui.space()
		cvui.text('Another text')
		cvui.space(40)
		cvui.text('End of column 2')
		cvui.endColumn()

		# Add more text
		cvui.text('this is the ')
		cvui.text('end of the row!')
		cvui.endRow()

		# Here is another nested row/column
		cvui.beginRow(frame, 50, 300, 100, 150)
		
		# If you don't want to calculate the size of any row/column WITHIN
		# a begin*()/end*() block, just use negative width/height when
		# calling beginRow() or beginColumn() (or don't provide width/height at all!)

		# For instance, the following column will have its width/height
		# automatically adjusted according to its content.
		cvui.beginColumn()
		cvui.text('Column 1')
		cvui.button('button with very large label')
		cvui.text('End of column 1')
		cvui.endColumn()

		# Add two pieces of text
		cvui.text('Hi again,')
		cvui.text('its me!')

		# Start a new column
		cvui.beginColumn()
		cvui.text('Column 2')
		cvui.button('btn')
		cvui.space()
		cvui.text('text')
		cvui.button('btn2')
		cvui.text('text2')
		if cvui.button('&Quit'):
			break
		cvui.endColumn()

		# Add more text
		cvui.text('this is the ')
		cvui.text('end of the row!')
		cvui.endRow()

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
