---
layout: default
title: window
---

# Window

`cvui::window()` renders a window (a block with a title and a body). The signature of the function is:

```cpp
void window (
    cv::Mat& theWhere,
    int theX,
    int theY,
    int theWidth,
    int theHeight,
    const cv::String& theTitle
)
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theWidth` is the width of the window, `theHeight` is the height of the window, and `theTitle` is the text displayed as the title of the window.

Below is an example showing a window. The result on the screen is shown in Figure 1.

```cpp
cvui::window(frame, 60, 10, 130, 90, "Title");
```

![Window]({{ site.url }}/img/window.png)
<p class="img-caption">Figure 1: window component.</p>

<code>cvui::window()</code> is useful to be used as a background for other UI components, particularly to distinguish them from other elements on the screen. Below is an illustration of `cvui::window()` used as background for another component:

![Window background for other UI components]({{ site.url }}/img/canny-ui.png)
<p class="img-caption">Figure 2: <code>cvui::window()</code> used as background for other UI components.</p>

## Learn more

Check the [main-app](https://github.com/Dovyski/cvui/tree/master/example/src/main-app) and [canny](https://github.com/Dovyski/cvui/tree/master/example/src/canny) examples for more information about window.
