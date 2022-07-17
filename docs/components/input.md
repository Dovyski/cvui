---
layout: default
title: input
---

# Input

`cvui::input()` renders a textfield that can be used by users to enter data. The signature of the function is:

```cpp
int input(
    cv::Mat& theWhere,
    int theX,
    int theY,
    int theWidth,
    const cv::String& theName,
    cv::String& theValue,
    double theFontScale = 0.5);
```

where `theWhere` is the image/frame where the input will be rendered, `theX` is the position X, `theY` is the position Y,  `theWidth` the size of the input (in pixels), `theName` is a unique name of the input, `theValue` is content of the input, and `theFontScale` size of the text.

Below is an example showing an input. The result on the screen is shown in Figure 1.

```cpp
cv::String inputValue = "123";
cvui::input(frame, 40, 40, 100, "uniqueName", inputValue);
```

![Input]({{ site.url }}/img/input.png)
<p class="img-caption">Figure 1: input component.</p>

When the user interacts with the input, the value of `theValue` is updated accordingly.

It is importat that the string you use for `theName` is unique to each input. Any string can be used, e.g. `input_01`, `myInput`, `aabbb33`. This string will be used to control focus, so non-unique input name (for instance, already used by another input) will cause problems with focus.

`cvui::input()` returns an integer that corresponds to the last keyboard key pressed inside the input (it is an ASCII code). To make things easier, cvui comes with constants to map the most important keys. Those constants are `cvui::KEY_*`. For instance, the `cvui::KEY_ENTER` identifies the enter key.

Using the value returned by `cvui::input()`, you can detect when a particular key was pressed and act upon this. For instance, to collect the value of the input when enter is pressed:

```cpp
cv::String inputValue = "123";

int key = cvui::input(frame, 40, 40, 100, "myInput", inputValue);

if (key == cvui::KEY_ENTER) {
    // Enter was pressed, do something with the input value
    std::cout << inputValue;
}
```

If no key was pressed within the input, `cvui::KEY_NONE` is returned.

## Learn more

Check the [input](https://github.com/Dovyski/cvui/tree/master/example/src/input) example for more information about the input. The [input-multiple](https://github.com/Dovyski/cvui/tree/master/example/src/input-multiple) show how to use several inputs at the same time.

The [input-detect-key](https://github.com/Dovyski/cvui/tree/master/example/src/input-detect-key) and [input-change-counter](https://github.com/Dovyski/cvui/tree/master/example/src/input-change-counter) show how to detect key presses within an input, and how to react upon it.
