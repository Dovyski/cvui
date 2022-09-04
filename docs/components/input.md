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
    const cv::String theName,
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

It is importat that the string you use for `theName` is unique to each input. Any string can be used, e.g. `input_01`, `myInput`, `aabbb33`. This string will be used to control focus, so a non-unique one (for instance, one already used by another input) will cause problems with focus.

`cvui::input()` returns an integer that corresponds to the last keyboard key pressed inside the input (it is an ASCII code). Using the value returned by `cvui::input()`, you can detect when a particular key was pressed and act upon this:

```cpp
cv::String inputValue = "123";

int key = cvui::input(frame, 40, 40, 100, "myInput", inputValue);

if (key == cvui::KEY_ENTER) {
    // Enter was pressed, do something with the input value
    std::cout << inputValue;
}
```

The example above collects the value of the input when <kbd>Enter</kbd> is pressed.

To make things easier, cvui comes with constants to map the most important keys. Those constants are `cvui::KEY_*`. For instance, the `cvui::KEY_ENTER` identifies the <kbr>Enter</kbr> key.

If no key was pressed within the input, `cvui::KEY_NONE` is returned.

Currently, the following keys are mapped:

Key | constant
--- | ---
<kbd>Left arrow</kbd> | `cvui::KEY_ARROW_LEFT`
<kbd>Right arrow</kbd> | `cvui::KEY_ARROW_RIGHT`
<kbd>Up arrow</kbd> | `cvui::KEY_ARROW_UP`
<kbd>Down arrow</kbd> | `cvui::KEY_ARROW_DOWN`
<kbd>Enter</kbd> | `cvui::KEY_ENTER`
<kbd>Backspace</kbd> | `cvui::KEY_BACKSPACE`
<kbd>Tab</kbd> | `cvui::KEY_TAB`
<kbd>Delete</kbd> | `cvui::KEY_DELETE`
<kbd>End</kbd> | `cvui::KEY_END`
<kbd>Home</kbd> | `cvui::KEY_HOME`

## Learn more

Check the [input](https://github.com/Dovyski/cvui/tree/master/example/src/input) example for more information about the input. The [input-multiple](https://github.com/Dovyski/cvui/tree/master/example/src/input-multiple) show how to use several inputs at the same time.

The [input-detect-key](https://github.com/Dovyski/cvui/tree/master/example/src/input-detect-key) and [input-change-counter](https://github.com/Dovyski/cvui/tree/master/example/src/input-change-counter) show how to detect key presses within an input, and how to react upon it.
