---
layout: default
title: trackbar
---

# Trackbar

`cvui::trackbar()` renders a trackbar for numeric values that users can increase/decrease by clicking and/or dragging the marker right or left. The signature of the function is:

```cpp
template <typename T>
bool trackbar (
    cv::Mat& theWhere,
    int theX,
    int theY,
    int theWidth,
    T *theValue,
    T theMin,
    T theMax,
    int theSegments = 1,
    const char *theLabelFormat = "%.1Lf",
    unsigned int theOptions = 0,
    T theDiscreteStep = 1
)
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theWidth` is the width of the trackbar, `theValue` is the current value of the trackbar, `theMin` is the minimum value allowed for the trackbar, `theMax` is the maximum value allowed for the trackbar.

The parameter `theValue`  will be modified when the user interacts with the trackbar. Any numeric type can be used, e.g. `float`, `double`, `long double`, `int`, `char`, `uchar`.

`cvui::trackbar()` returns `true` when the value of the trackbar changed, or `false` if the value remains the same since the last interaction.

<div class="notice--warning"><strong>IMPORTANT:</strong> <code>cvui::trackbar()</code> uses C++ templates, so it is imperative that you make it very explicit the type of parameters <code>theValue</code>, <code>theMin</code>, <code>theMax</code> and <code>theStep</code>, otherwise you might end up with weird compilation errors.</div>

Below is an example showing a trackbar. The result on the screen is shown in Figure 1.

```cpp
double value = 12.4;
cvui::trackbar(frame, 40, 30, 220, &value, (double)10.0, (double)15.0);
```

![Trackbar]({{ site.url }}/img/trackbar.png)
<p class="img-caption">Figure 1: trackbar component using double values.</p>

## Customization

Trackbars can be highly customized. Parameter `theSegments` indicates the number of segments the trackbar will have (default is `1`). Segments can be seen as groups of numbers in the scale of the trackbar. For example, 1 segment means a single groups of values (no extra labels along the scale), 2 segments mean the trackbar values will be divided in two groups and a label will be placed at the middle of the scale.

Parameter `theLabelFormat` is the formatting string that will be used to render the labels, e.g. `%.2Lf` (Lf *not* lf). No matter the type of the `theValue` param, internally `cvui::trackbar()` stores it as a `long double`, so the formatting string will *always* receive a `long double` value to format. If you are using a trackbar with integers values, for instance, you can supress decimals using a formating string such as `%.0Lf` to format your labels.

Parameter `theOptions` provide options to customize the behavior/appearance of the trackbar, expressed as a bitset. Available options are defined as `TRACKBAR_` constants and they can be combined using the bitwise `|` operand. Available options are:

* `TRACKBAR_HIDE_SEGMENT_LABELS`: do not render segment labels, but do render min/max labels;
* `TRACKBAR_HIDE_STEP_SCALE`: do not render the small lines indicating values in the scale;
* `TRACKBAR_DISCRETE`: changes of the trackbar value are multiples of `theDiscreteStep` param;
* `TRACKBAR_HIDE_MIN_MAX_LABELS`: do not render min/max labels;
* `TRACKBAR_HIDE_VALUE_LABEL`: do not render the current value of the trackbar below the moving marker;
* `TRACKBAR_HIDE_LABELS`: do not render labels at all.

The parameter `theDiscreteStep` is the amount that the trackbar marker will increase/decrease when the marker is dragged right/left (if option `TRACKBAR_DISCRETE` is active). Figures 2 and 3 illustrate the differences.

![Trackbar without discrete step]({{ site.url }}/img/trackbar.gif)
<p class="img-caption">Figure 2: trackbar component without discrete step.</p>

![Trackbar using a discrete step]({{ site.url }}/img/trackbar-discrete.gif)
<p class="img-caption">Figure 3: trackbar component using a discrete step.</p>

## Learn more

Check the [sparkline](https://github.com/Dovyski/cvui/tree/master/example/src/sparkline) example for more information about sparklines.
