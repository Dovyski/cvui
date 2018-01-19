---
layout: default
title: counter
---

# Counter

`cvui::counter()` renders a counter for integer (or double) values that users can increase/decrease by clicking up and down arrows. The signature of the functions are:

```cpp
int counter (
    cv::Mat& theWhere,
    int theX,
    int theY,
    int *theValue,
    int theStep = 1,
    const char *theFormat = "%d"
)
```

```cpp
double counter (
    cv::Mat& theWhere,
    int theX,
    int theY,
    double *theValue,
    double theStep = 0.5,
    const char *theFormat = "%.2f"
)
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theValue` is the current value of the counter, `theStep` is the amount that should be increased/decreased when the user interacts with the counter buttons, and `theFormat` is how the value of the counter should be presented, as it was printed by `stdio's printf()`. E.g. `"%d"` means the value will be displayed as an integer, `"%0d"` integer with one leading zero, etc.

`cvui::counter()` returns a number that corresponds to the current value of the counter.

Below is an example showing a counter. The result on the screen is shown in Figure 1.

```cpp
int count = 2;
cvui::counter(frame, 90, 50, &count);
```

![Counter]({{ site.url }}/img/counter.png)
<p class="img-caption">Figure 1: counter component.</p>

## Learn more

Check the [main-app](https://github.com/Dovyski/cvui/tree/master/example/src/main-app) example for more information about counter.
