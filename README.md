cvui
=====
A (very) simple UI lib built on top of OpenCV drawing primitives. Sometimes you don't have (or don't want) to use OpenGL and/or Qt in your OpenCV application!

![image](https://raw.githubusercontent.com/Dovyski/depository/master/cvui.png)

Features
--------
- Lightweight and simple to use user interface.
- No external dependencies (except OpenCV).
- Friendly and C-like API (no classes/objects, etc).
- MIT licensed.

Build
-----
The only dependency is OpenCV (version 3.0), which you are probably already using. Just add `cvui.h` and `cvui.cpp` to your project and you are ready to go.

Usage
-----
Check the [examples](examples) folder for some code, but the general idea is the following:

```
#define WINDOW_NAME		"CVUI Test"

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(250, 600, CV_8UC3);
	bool checked = false;
	int count = 0;

	cv::namedWindow(WINDOW_NAME);
	cvui::init(WINDOW_NAME);

	while (true) {
		frame = cv::Scalar(49, 52, 49);

		cvui::text(frame, 50, 30, "Hey there!");
		cvui::text(frame, 200, 30, "Use hex 0xRRGGBB colors easily", 0.4, 0xff0000);

		if (cvui::button(frame, 50, 50, "Button")) {
			std::cout << "Button clicked!" << std::endl;
		}

		cvui::window(frame, 50, 100, 120, 100, "Window");
		cvui::counter(frame, 200, 100, &count);
		cvui::checkbox(frame, 200, 150, "Checkbox", &checked);

		cvui::update();

		cv::imshow(WINDOW_NAME, frame);
		cv::waitKey(30);
	}

	return 0;
}
```

License
-----
Copyright (c) 2016 Fernando Bevilacqua. Licensed under the MIT license.
