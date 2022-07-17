---
layout: default
title: advanced-headless
---

# Headless mode
Sometimes you want your application to run without showing any window. This is useful for automated testing, CI/CD, or for running your application as a CLI.

Since version `2.9.0`, cvui comes with a headless mode. When running in headless mode, cvui will not render anything to the screen and it will not process interactions such as mouse clicks.

## Using headless mode

You can enable the headless mode by calling `cvui::init()` passing `true` to the `theHeadless` param. Additionally, you can use the `cvui::headless()` function to enable or disable the headless mode at any time.

The example below shows how to use the headless mode.

```cpp
int main(int argc, const char *argv[])
{
    cv::Mat frame = cv::Mat(300, 600, CV_8UC3);
    bool state = false;

    std::cout << "Rendering cvui GUI in headless mode." << std::endl;

    // Init cvui and tell it to create a (virtual) window.
    // The last flag 'headless' is 'true', so *no* actual GUI windows will be created.
    cvui::init(WINDOW_NAME, 1, true, true);

    while (true) {
        frame = cv::Scalar(49, 52, 49);

        // Show the coordinates of the mouse pointer on the screen
        cvui::text(frame, 10, 30, "Hello, World!");

        // Create a checkbox that will never be clicked. This is still OK in headless mode.
        cvui::checkbox(frame, 10, 50, "A checkbox that will never be clicked in headless mode", &state);

        // Update and show everything on the screen
        // This is still OK in headless mode.
        cvui::imshow(WINDOW_NAME, frame);

        // Terminate the loop for the sake of this example, but you could
        // use something like  `if (cv::waitKey(20) == 27) ` here, it is still OK in headless mode.
        break;
    }

    // Create an image with the result of the rendering of cvui.
    // It's like a screenshot of the GUI.
    cv::imwrite("headless_frame.png", frame);

    return 0;
}

```

When the example above is run, it will not display any window.  with the text "Hello, World!" and a checkbox. The checkbox will never be clicked.

![Input]({{ site.url }}/img/headless_frame.png)
<p class="img-caption">Figure 1: content of the <em>headless_frame.png</em> produced by the example above.</p>

## Enable/disable and checking if enabled

You can enable or disable the headless mode at any time by calling `cvui::headless(true)` or `cvui::headless(false)`. Additionally, if you want to check if cvui is running in headless mode, just call `cvui::headless()` without any parameters:

```cpp
// Enable headless mode
cvui::headless(true);

if (cvui::headless()) {
    // cvui is running in headless mode
}

// Disable headless mode
cvui::headless(false);
```

## Learn more

Check the [headless](https://github.com/Dovyski/cvui/tree/master/example/src/headless) example for more information about the headless mode.