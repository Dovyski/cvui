/*
 A (very) simple UI lib built on top of OpenCV drawing primitives.

 Copyright (c) 2016 Fernando Bevilacqua <dovyski@gmail.com>
 Licensed under the MIT license.
*/

#ifndef _CVUI_H_
#define _CVUI_H_

#include "opencv2/core/core.hpp"
#include <string>

namespace cvui
{

// Initializes the library. You must inform the maximum width and
// height of the window where the lib will render the UI components.
void init(const cv::String& theWindowName);

// Display a button. Returns true everytime the user clicks the button.
bool button(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel);
bool button(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theLabel);

// Display a checkbox. You can use the state parameter to monitor if the
// checkbox is checked or not.
bool checkbox(cv::Mat& theWhere, int theX, int theY, const cv::String& theLabel, bool *theState);

// Display a piece of text.
void text(cv::Mat& theWhere, int theX, int theY, const cv::String& theText, double theFontScale);

// Display a counter that the user can increase/descrease by clicking
// the up and down arrows.
int counter(cv::Mat& theWhere, int theX, int theY, int *theValue);

// Display an overlay (a block with a title and a transparent body).
void window(cv::Mat& theWhere, int theX, int theY, int theWidth, int theHeight, const cv::String& theTitle);

// You need to call this function after you are done adding/manipulating
// UI elements in order for them to react to mouse interactions.
void update();

// Internally used to handle mouse events
void handleMouse(int theEvent, int theX, int theY, int theFlags, void* theData);

} // namespace cvui

#endif // _CVUI_H_