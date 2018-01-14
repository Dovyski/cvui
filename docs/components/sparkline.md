---
layout: default
title: sparkline
---

# Sparkline

`cvui::sparkline()` renders the values of a `std::vector<double>` as a sparkline. The signature of the function is:

```cpp
void sparkline (
    cv::Mat& theWhere,
    std::vector<double>& theValues,
    int theX,
    int theY,
    int theWidth,
    int theHeight,
    unsigned int theColor = 0x00FF00
)
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theWidth` is the width of the sparkline, `theHeight` is the height of the sparkline, and `theColor` is the color of sparkline in the format `0xRRGGBB`, e.g. `0xff0000` for red.

<div class="notice--info"><strong>Tip:</strong> if an empty vector is provided to <code>cvui::sparkline()</code>, a message informing about the lack of data will be displayed instead of the sparkline.</div>

Below is an example showing a sparkline. The result on the screen is shown in Figure 1.

```cpp
std::vector<double> values;
for (std::vector<double>::size_type i = 0; i < 30; i++) {
  values.push_back(rand() + 0.);
}

cvui::sparkline(frame, values, 10, 10, 280, 100);
```

![Sparkline]({{ site.url }}/img/sparkline.png)
<p class="img-caption">Figure 1: sparkline component.</p>

## Learn more

Check the [sparkline](https://github.com/Dovyski/cvui/tree/master/example/src/sparkline) example for more information about sparklines.
