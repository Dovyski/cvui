#
# This is a demo application to showcase the sparkline components of cvui.
# Sparklines are quite useful to display data, e.g. FPS charts.
#
# Copyright (c) 2018 Fernando Bevilacqua <dovyski@gmail.com>
# Licensed under the MIT license.
#

import numpy as np
import cv2
import cvui
import random

WINDOW_NAME	= 'Sparkline'

def load(thePath):
	file = open(thePath, 'r')

	if file == False:
		print('Unable to open file: ', thePath)
		sys.exit(-1)

	data = []
	line = file.readline() 

	while line:
		parts = line.split('\t')
		data.append(float(parts[1]))
		line = file.readline() 

	return data


def main():
	frame = np.zeros((600, 800, 3), np.uint8)

	# Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui.init(WINDOW_NAME)

	# Load some data points from a file
	points = load('sparkline.csv')
	
	# Create less populated sets
	few_points = []
	no_points = []
	
	for i in range(0, 30):
		few_points.append(random.uniform(0., 300.0))
	
	while (True):
		# Fill the frame with a nice color
		frame[:] = (49, 52, 49)

		# Add 3 sparklines that are displaying the same data, but with
		# different width/height/colors.
		cvui.sparkline(frame, points, 0, 0, 800, 200);
		cvui.sparkline(frame, points, 0, 200, 800, 100, 0xff0000);
		cvui.sparkline(frame, points, 0, 300, 400, 100, 0x0000ff);
		
		# Add a sparkline with few points
		cvui.sparkline(frame, few_points, 10, 400, 790, 80, 0xff00ff);

		# Add a sparkline that has no data. In that case, cvui will
		# render it with a visual warning.
		cvui.sparkline(frame, no_points, 10, 500, 750, 100, 0x0000ff);

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
