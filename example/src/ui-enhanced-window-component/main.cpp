/*
This application showcases how the window component of cvui can be
enhanced, i.e. make it movable and minimizable.

Authors:
	ShengYu - https://github.com/shengyu7697
	Amaury Bréhéret - https://github.com/abreheret

Contributions:
	Fernando Bevilacqua <dovyski@gmail.com>

Code licensed under the MIT license.
*/

#include <opencv2/opencv.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

// Include the enhanced cvui window component
#include "EnhancedWindow.h"

#define WINDOW_NAME    "CVUI Enhanced Window Component"

int main(int argc, const char *argv[])
{
	cv::Mat frame;
	int value = 50;
	
	const int settingsPosX = 20;
    const int settingsPosY = 80;
    const int settingsWidth = 200;
    const int settingsHeight = 120;
    const int infoPosX = 250;
    const int infoPosY = 80;
    const int infoWidth = 330;
    const int infoHeight = 60;
    
    EnhancedWindow settings(settingsPosX, settingsPosY, settingsWidth, settingsHeight, "Settings");
	EnhancedWindow info(infoPosX, infoPosY, infoWidth, infoHeight, "Info");

    // Init cvui and tell it to create an OpenCV window, i.e. cv::namedWindow(WINDOW_NAME).
    cvui::init(WINDOW_NAME);
    
    double scaling = 1.0;
    double currentScaling = -1;
    
    while (true) {
        const double fontScale = scaling*cvui::DEFAULT_FONT_SCALE;

        if (scaling != currentScaling) {
            frame = cv::Mat(std::lround(scaling * 600), std::lround(scaling * 800), CV_8UC3);
            
            settings.setPosX(std::lround(scaling*settingsPosX));
            settings.setPosY(std::lround(scaling*settingsPosY));
            settings.setWidth(std::lround(scaling*settingsWidth));
            settings.setHeight(std::lround(scaling*settingsHeight));
            settings.setFontScale(fontScale);
            
            info.setPosX(std::lround(scaling*infoPosX));
            info.setPosY(std::lround(scaling*infoPosY));
            info.setWidth(std::lround(scaling*infoWidth));
            info.setHeight(std::lround(scaling*infoHeight));
            info.setFontScale(fontScale);

            currentScaling = scaling;
        }
                
		// Fill the frame with a nice color
		frame = cv::Scalar(49, 52, 49);

		// Place some instructions on the screen regarding the
		// settings window
		cvui::text(frame, std::lround(scaling * 20), std::lround(scaling * 20), "The Settings and the Info windows below are movable and minimizable.", fontScale);
		cvui::text(frame, std::lround(scaling * 20), std::lround(scaling * 40), "Click and drag any window's title bar to move it around.", fontScale);

		// Render a movable and minimizable settings window using
		// the EnhancedWindow class.
		settings.begin(frame);
            if (!settings.isMinimized()) {
                cvui::text("Adjust something", fontScale);
				cvui::space(std::lround(scaling * 10)); // add 10px of space between UI components
                cvui::trackbar(settings.width() - std::lround(scaling * 20), &value, 5, 150, 1, "%.1Lf", 0, 1, fontScale);
            }
		settings.end();

		// Render a movable and minimizable settings window using
		// the EnhancedWindow class.
		info.begin(frame);
		if (!info.isMinimized()) {
			cvui::text("Moving and minimizable windows are awesome!", fontScale);
		}
		info.end();

		cvui::counter(frame, std::lround(scaling * 600), std::lround(scaling * 500), &scaling, 0.1, "%.1f", fontScale);

        cvui::printf(frame, std::lround(scaling * 620), std::lround(scaling * 530), fontScale, 0xCECECE, "Scaling");
        
		// Update all cvui internal stuff, e.g. handle mouse clicks, and show
		// everything on the screen.
        cvui::imshow(WINDOW_NAME, frame);

        // Check if ESC was pressed
        if (cv::waitKey(30) == 27) {
            break;
        }
    }

    return 0;
}
