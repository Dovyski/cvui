/*
 This is application uses the mouse API to dynamically create a ROI
 for image visualization.

 Copyright (c) 2017 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#ifndef _CLASS1_H_
#define _CLASS1_H_

class Class1 {
public:
	bool checked;

	Class1();
	void renderInfo(cv::Mat& frame);
};

#endif // _CLASS1_H_
