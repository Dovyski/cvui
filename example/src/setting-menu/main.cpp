/*
This is a demo application to showcase the UI components of cvui.

Code licensed under the MIT license, check LICENSE file.
*/

#include <opencv2/opencv.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME    "CVUI Setting Menu"

class Setting
{
public :
    Setting(int x, int y, int width, int height, const cv::String& title = "Setting") :
        mX(x),
        mY(y),
        mWidth(width),
        mHeight(height),
        mOldHeight(height),
        mTitle(title),
        mDeltaY(0),
        mDeltaX(0),
        mIsMove(false),
        mMinimize(false) {
    }

    void begin(cv::Mat &frame) {
        mHeight = mMinimize ? 20 : mOldHeight;

        if (mIsMove == false && cvui::mouse(cvui::DOWN) && cvui::mouse().inside(cv::Rect2i(mX, mY, mWidth, 20))) {
            mDeltaX = cvui::mouse().x - mX;
            mDeltaY = cvui::mouse().y - mY;
            mIsMove = true;
        } else if (mIsMove && cvui::mouse(cvui::IS_DOWN)) {
            mX = cvui::mouse().x - mDeltaX;
            mY = cvui::mouse().y - mDeltaY;
        } else { //if (cvui::mouse(cvui::UP)) {
            mIsMove = false;
            mX = MAX(0, mX);
            mY = MAX(0, mY);
            mX = MIN(frame.cols - mWidth, mX);
            mY = MIN(frame.rows - 20    , mY);
        }

        cvui::window(frame, mX, mY, mWidth, mHeight, mTitle);
        if (cvui::button(frame, mX + mWidth - 20, mY + 1, 18, 18, mMinimize ? "+" : "-")) {
            mMinimize ^= 1;
        }
        cvui::beginRow(frame, mX + 10, mY + 40, mWidth - 20, mHeight - 20);
        cvui::beginColumn(mWidth - 10, mHeight - 20);
    }

    void end() {
        cvui::endColumn();
        cvui::endRow();
    }

    int width() const {
        return mWidth;
    }

    int height() const {
        return mHeight;
    }

    void setWidth(int w) {
        mWidth = w;
    }

    void setHeight(int h) {
        mHeight = h;
    }

    bool isMinimize() {
        return mMinimize;
    }

private:
    int mX;
    int mY;
    int mWidth;
    int mHeight;
    int mOldHeight;
    cv::String mTitle;
    int mDeltaY;
    int mDeltaX;
    bool mIsMove;
    bool mMinimize;
};

int main(int argc, const char *argv[])
{
    cv::Mat image = cv::imread("fruits.jpg");
    cv::Mat frame = image.clone();
    int low_threshold = 50, high_threshold = 150;
    bool use_canny = false;

    // Init cvui and tell it to create a OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
    cvui::init(WINDOW_NAME);
    Setting setting1(10, 50, 200, 150, "Setting1");
    while (true) {
        // Should we apply Canny edge?
        if (use_canny) {
            // Yes, we should apply it.
            cv::cvtColor(image, frame, CV_BGR2GRAY);
            cv::Canny(frame, frame, low_threshold, high_threshold, 3);
        } else {
            // No, so just copy the original image to the displaying frame.
            image.copyTo(frame);
        }

        setting1.begin(frame);
            if (!setting1.isMinimize()) {
                cvui::checkbox("Use Canny Edge", &use_canny);
                cvui::trackbar(setting1.width() - 20, &low_threshold, 5, 150);
                cvui::trackbar(setting1.width() - 20, &high_threshold, 80, 300);
            }
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
