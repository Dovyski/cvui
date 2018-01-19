---
layout: default
title: usage
---

# Usage

Below are a few steps you need to perform to work with cvui.

## 1. Include `cvui.h`

Download the [latest release](https://github.com/Dovyski/cvui/releases/latest) and place `cvui.h` along with the files of your project. Include `cvui.h` in one of your C++ files as follows:

```cpp
#define CVUI_IMPLEMENTATION
#include "cvui.h"
```

<div class="notice--warning">
<strong>IMPORTANT:</strong> if you are using <code>cvui.h</code> in multiple files, e.g. different layout classes, you need to use <code>#define CVUI_IMPLEMENTATION</code> in <strong>one (and only one) of your C++ files</strong>. All other files should include <code>cvui.h</code> without <code>#define CVUI_IMPLEMENTATION</code>. E.g:

{% highlight c++ %}
// File: main.cpp
#define CVUI_IMPLEMENTATION      <-- CVUI_IMPLEMENTATION defined in one (and only one) C++ source file.
#include "cvui.h"
// (...)
/////////////////////////////////////////////

// File: another.cpp
#include "cvui.h"
// (...)
/////////////////////////////////////////////

// File: MyClass.hpp
#include "cvui.h"
// (...)
/////////////////////////////////////////////
{% endhighlight %}
</div>

<div class="notice--info"><strong>Tip:</strong> check the <a href="https://github.com/Dovyski/cvui/tree/master/example/src/multiple-files">multiple-files</a> example to learn more about the use of cvui in projects with multiple files that include <code>cvui.h</code>.</div>

## 2. Initialize cvui

Before using cvui, you need to call `cvui::init()` to initialize it. The easiest way is to initialize cvui and tell it to create any OpenCV window that will be used. Below is an example where cvui is initialized and a window is created:

```cpp
#include <opencv2/opencv.hpp>
#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW1_NAME "Window 1"

int main() {
  // Tell cvui to init and create a window
  cvui::init(WINDOW1_NAME);

  while(true) {
    // your app logic here

    if (cv::waitKey(20) == 27) {
      break;
    }
  }

  return 0;
}
```

<div class="notice--info"><strong>Tip:</strong> if you need to use cvui with multiple windows, or you want more control over the process of creating windows, check the <a href="{{ site.url }}/advanced-multiple-windows">Multiple OpenCV windows</a> page and the <a href="https://github.com/Dovyski/cvui/tree/master/example/src/multiple-windows">multiple-windows</a> and <a href="https://github.com/Dovyski/cvui/tree/master/example/src/multiple-windows-complex">multiple-windows-complex</a> examples.</div>

## 3. Render cvui components

All cvui components are rendered to a `cv::Mat`. Below is an example showing how to render a `"Hello world"` message on a `cv::Mat` named `frame`:

```cpp
#include <opencv2/opencv.hpp>
#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW1_NAME "Window 1"

int main() {
  cvui::init(WINDOW1_NAME);

  // Create a frame
  cv::Mat frame = cv::Mat(cv::Size(400, 200), CV_8UC3);

  while(true) {
    // clear the frame
    frame = cv::Scalar(49, 52, 49);

    // render a message in the frame at position (10, 15)
    cvui::text(frame, 10, 15, "Hello world!");

    if (cv::waitKey(20) == 27) {
      break;
    }
  }

  return 0;
}
```

## 3. Show (window) content

After rendering your components, show the final result using `cvui::imshow()`, which is cvui's improved version of OpenCV's `cv::imshow()`:

```cpp
#include <opencv2/opencv.hpp>
#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW1_NAME "Window 1"

int main() {
  cvui::init(WINDOW1_NAME);
  cv::Mat frame = cv::Mat(cv::Size(400, 200), CV_8UC3);

  while(true) {
    frame = cv::Scalar(49, 52, 49);
    cvui::text(frame, x, y, "Hello world!");

    // Show window content
    cvui::imshow(WINDOW1_NAME, frame);

    if (cv::waitKey(20) == 27) {
      break;
    }
  }
  return 0;
}
```

When you use `cvui::imshow()` instead of `cv::imshow()`, cvui will not only show the content, but update its internal structures to ensure all UI interactions work.

If you want to use `cv::imshow()`, you must call `cvui::update()` before `cv::imshow()` and after you are finished invoking cvui components, so cvui can perform its internal processing to handle mouse interactions. E.g.

```cpp
#include <opencv2/opencv.hpp>
#define CVUI_IMPLEMENTATION
#include "cvui.h"

#define WINDOW_NAME "CVUI Test"

int main() {
  cvui::init(WINDOW1_NAME);
  cv::Mat frame = cv::Mat(cv::Size(400, 200), CV_8UC3);

  while(true) {
    frame = cv::Scalar(49, 52, 49);
    cvui::text(frame, x, y, "Hello world!");

    // Update cvui internal stuff
    cvui::update();

    // Show window content
    cv::imshow(WINDOW1_NAME, frame);

    if (cv::waitKey(20) == 27) {
      break;
    }
  }

  return 0;
}
```

## (Optional) 4. Disable cvui compilation messages

The compilation process of cvui will produce a few console messages to help developers debug possible problems, e.g. inclusion of `cvui.h` using `#define CVUI_IMPLEMENTATION`. The two possible messages are:

* *cvui.h: compiling implementation because of CVUI_IMPLEMENTATION. See: https://dovyski.github.io/cvui/usage/*
* *cvui.h: implementation skipped. Ensure one of your C++ files included cvui.h after a #define CVUI_IMPLEMENTATION. See: https://dovyski.github.io/cvui/usage/*

You can disable such compilation messages by defining `CVUI_DISABLE_COMPILATION_NOTICES` before including `cvui.h`. E.g.:

```cpp
#include <opencv2/opencv.hpp>

#define CVUI_DISABLE_COMPILATION_NOTICES
#define CVUI_IMPLEMENTATION
#include "cvui.h"
```

## Learn more

Check out the [examples]({{ site.url }}/examples) page for more usage demonstrations of cvui.
