/*
This is a demo application to showcase the UI components of cvui.

Code licensed under the MIT license, check LICENSE file.
*/

#include <opencv2/opencv.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"CVUI Canny Edge"


class Setting {
    int  _x_setting ;
    int  _y_setting ;
    int  _y_delta   ;
    int  _x_delta   ;
    bool _is_move   ;
    int  _width     ;
    int  _height    ;
    cv::String _name;
public :
    Setting(int x,int y,int width,int height,const char * name = "Setting") {
        _x_setting = x;
        _y_setting = y;
        _y_delta = 0;
        _x_delta = 0;
        _is_move = false;
        _width = width;
        _height = height;
        _name = name;
    }

    void begin(cv::Mat &frame) {
        if (_is_move == false && cvui::mouse(cvui::DOWN) && cvui::mouse().inside(cv::Rect2i(_x_setting, _y_setting, _width, 20))) {
            _x_delta = cvui::mouse().x - _x_setting;
            _y_delta = cvui::mouse().y - _y_setting;
            _is_move = true;
        } else if (_is_move && cvui::mouse(cvui::IS_DOWN)) {
            _x_setting = cvui::mouse().x - _x_delta;
            _y_setting = cvui::mouse().y - _y_delta;
        } else { //if (cvui::mouse(cvui::UP)) {
            _is_move = false;
            _x_setting = MAX(0, _x_setting);
            _y_setting = MAX(0, _y_setting);
            _x_setting = MIN(frame.cols-_width , _x_setting);
            _y_setting = MIN(frame.rows-20     , _y_setting);
        }
        cvui::window(frame, _x_setting, _y_setting, _width, _height, _name.c_str());
        cvui::beginRow(frame, _x_setting + 10, _y_setting + 40, _width -20, _height-20);
        cvui::beginColumn(_width-10, _height-20);
    }

    void end() {
        cvui::endColumn();
        cvui::endRow();
    }

    int width() const {
        return _width;
    }
    int height() const {
        return _height;
    }
};

int main(int argc, const char *argv[])
{
	cv::Mat lena = cv::imread("lena.jpg");
	cv::Mat frame = lena.clone();
	int low_threshold = 50, high_threshold = 150;
	bool use_canny = false;

	// Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
	cvui::init(WINDOW_NAME);
    Setting setting1(10,50,200,150,"Setting1");
	while (true) {
		// Should we apply Canny edge?
		if (use_canny) {
			// Yes, we should apply it.
			cv::cvtColor(lena, frame, CV_BGR2GRAY);
			cv::Canny(frame, frame, low_threshold, high_threshold, 3);
		} else {
			// No, so just copy the original image to the displaying frame.
			lena.copyTo(frame);
		}

        setting1.begin(frame);
		    cvui::checkbox("Use Canny Edge", &use_canny);
		    cvui::trackbar(setting1.width()-20, &low_threshold, 5, 150);
		    cvui::trackbar(setting1.width()-20, &high_threshold, 80, 300);
        setting1.end();

		cvui::update();

		cv::imshow(WINDOW_NAME, frame);

		// Check if ESC was pressed
		if (cv::waitKey(30) == 27) {
			break;
		}
	}

	return 0;
}