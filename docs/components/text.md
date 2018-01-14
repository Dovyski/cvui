---
layout: default
title: text
---

# Text

`cvui::text()` renders a string. The signature of the function is:

```cpp
void text (
    cv::Mat& theWhere,
    int theX,
    int theY,
    const cv::String& theText,
    double theFontScale = 0.4,
    unsigned int theColor = 0xCECECE
)
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theText` is the text content, `theFontScale` is the size of the text, and `theColor` is color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red.

Below is an example of the text component. The result on the screen is shown in Figure 1.

```cpp
cvui::text(frame, 90, 50, "Hello world");
```

![Text]({{ site.url }}/img/text.png)
<p class="img-caption">Figure 1: text component.</p>

## Learn more

Check the [main-app](https://github.com/Dovyski/cvui/tree/master/example/src/main-app) example for more information about text.
