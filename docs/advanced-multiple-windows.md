---
layout: default
title: advanced-multiple-windows
---

# Multiple OpenCV windows

If your project uses multiple OpenCV windows, e.g. show intermediary results, and those windows have cvui components, you need to perform a few extra steps to ensure UI components will work. The following sections will show you how to use cvui components in multiple windows.

## 1. Create the windows

cvui uses OpenCV `cv::setMouseCallback()` to monitor interactions on each window, so the windows your application use must exist before you call `cvui::init()`. That way cvui can set the callback on each one of them.

The easiest way is to let cvui create the windows for you in `cvui::init()`. Below is an example where `cvui::init()` is called with an array of window names, so cvui will create the windows automatically:

```cpp
#define WINDOW1_NAME "Window 1"
#define WINDOW2_NAME "Windows 2"
#define WINDOW3_NAME "Windows 3"
#define WINDOW4_NAME "Windows 4"

#include <opencv2/opencv.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

int main() {
  // Tell cvui to init and create 4 windows.
  const cv::String windows[] = { WINDOW1_NAME, WINDOW2_NAME, WINDOW3_NAME, WINDOW4_NAME };  
  cvui::init(windows, 4);

  while(true) {
    // your logic here
  }
}
```

## 1.1 (Optional) Create your own windows

If you want to create the windows youself, ensure you create them using `cv::namedWindow()` before calling `cvui::init()`.

When initializing cvui using `cvui::init()`, you still need to inform the name of a window (which will be the default window), then call `cvui::watch()` for each subsequent window to be monitored by cvui:

```cpp
#define WINDOW1_NAME "Window 1"
#define WINDOW2_NAME "Windows 2"
#define WINDOW3_NAME "Windows 3"
#define WINDOW4_NAME "Windows 4"

#include <opencv2/opencv.hpp>

#define CVUI_IMPLEMENTATION
#include "cvui.h"

int main() {
  // Create OpenCV windows
  cv::namedWindow(WINDOW1_NAME);
  cv::namedWindow(WINDOW2_NAME);
  cv::namedWindow(WINDOW3_NAME);
  cv::namedWindow(WINDOW4_NAME);

  // Init cvui, using WINDOW1_NAME as the default window.
  // The last parameter is false, informing cvui to not
  // create any new window.
  cvui::init(WINDOW1_NAME, -1, false);

  // Tell cvui to monitor the windows,
  // otherwise UI interactions will not work on them.
  cvui::watch(WINDOW2_NAME);
  cvui::watch(WINDOW3_NAME);
  cvui::watch(WINDOW4_NAME);

  while(true) {
    // your logic here
  }
}
```

## 2. Tell cvui about the window, then render it

When using cvui components with multiple windows, you need to inform cvui which window those compoments belong to. You do that by enclosing all cvui component calls between the pair `cvui::context(NAME)` and `cvui::imshow(NAME, frmae)`, where `NAME` is the name of the window being worked on.

The example below shows how to render a few components in two different window, e.g. `"window1"` and `"window2"`, assuming those windows were already created and cvui properly initialized before:

```cpp
// Create a frame for the windows
cv::Mat frame = cv::Mat(200, 500, CV_8UC3);

cvui::context("window1");                    // Inform cvui that the components to be rendered from now one belong to "window1"
cvui::text(frame, 10, 50, "Hello, window1");
cvui::imshow("window1", frame);              // update cvui interactions on window "window1" and show it

cvui::context("window1");                     // Inform cvui that the components to be rendered from now one belong to "window2"
cvui::text(frame, 5, 5, "Hey, window2");
cvui::imshow("window1", frame);               // update cvui interactions on window "window2"
```

## 2.1 (Optional) Fine control update and show

You can ignore `cvui::imshow()`, which is cvui's boosted version of `cv::imshow()`, but instead you want to be in control of the update and show of each window, e.g. by calling `cv::imshow()` yourself, you can do it.

In that case, you enclose all cvui component calls between the pair `cvui::context(NAME)` and `cvui::update(NAME)`, where `NAME` is the name of the window being worked on.

<div class="notice--info"><strong>NOTICE:</strong> in practice what <code>cvui::imshow()</code> does is to call <code>cvui::update()</code> followed by <code>cv::imshow()</code>, so you don't have to type it yourself.</div>

The example below shows how to separately update and render a few components in two different window, e.g. `"window1"` and `"window2"`, assuming those windows were already created and cvui properly initialized before:

```cpp
// Create a frame for this window and fill it with a nice color
cv::Mat frame = cv::Mat(200, 500, CV_8UC3);

cvui::context("window1");                     // Inform cvui that the components to be rendered from now one belong to "window1"
cvui::text(frame, 10, 50, "Hello, window1");
cvui::update("window1");                      // update cvui interactions on window "window1"

// Show the content of window "window1" on the screen
cvui::imshow("window1", frame);

cvui::context("window1");                     // Inform cvui that the components to be rendered from now one belong to "window2"
cvui::text(frame, 5, 5, "Hey, window2");
cvui::update("window1");                      // update cvui interactions on window "window2"

// Show the content of window "window2" on the screen
cvui::imshow("window2", frame);

```
