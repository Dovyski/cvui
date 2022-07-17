/*
This is application shows how to use the headless mode.

Copyright (c) 2017 Fernando Bevilacqua <dovyski@gmail.com>
Licensed under the MIT license.
*/

#include <iostream>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME	"Headless"
#define ENABLE_HEADLESS true

int main(int argc, const char *argv[])
{
	cv::Mat frame = cv::Mat(300, 600, CV_8UC3);
    bool state = false;

    // Init cvui and tell it to create a (virtual) window.
    // The last flag 'headless' is 'true', so *no* actual GUI windows will be created.
    std::cout << "Rendering cvui GUI in headless mode." << std::endl;
    cvui::init(WINDOW_NAME, 1, true, ENABLE_HEADLESS);


    while (true) {
        // Fill the frame with a nice color
        frame = cv::Scalar(49, 52, 49);

        // Show some text on the screen
        cvui::text(frame, 10, 30, "Hello, World!");

        // Create a checkbox that will never be clicked. This is still OK in headless mode.
        cvui::checkbox(frame, 10, 50, "A checkbox that will never be clicked in headless mode", &state);

        // Update and show everything on the screen
        // This is still OK in headless mode.
        cvui::imshow(WINDOW_NAME, frame);

        // This is still OK in headless mode.
        if (ENABLE_HEADLESS || cv::waitKey(20) == 27) {
            break;
        }
    }

    cv::imwrite("headless_frame.png", frame);
    std::cout << "Wrote headless_frame.png" << std::endl;

    return 0;
}
