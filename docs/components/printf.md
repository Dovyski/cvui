---
layout: default
title: printf
---

# printf

`cvui::printf()` renders a piece of text that can be formatted using C `printf()` style. The signature of the function is:

```cpp
void printf(cv::Mat& theWhere, int theX, int theY, const char *theFmt, ...);
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theFmt` is the formating string as it would be supplied for `stdio's printf()`, e.g. `"Text: %d and %f", 7, 3.1415`.

`cvui::printf()` is used pretty much as C's `printf()` function. Below is an example of the component, whose result on the screen is shown in Figure 1.

```cpp
double value = 3.14;
cvui::printf(frame, 90, 50, "value = %.2f", value);
```

![printf component]({{ site.url }}/img/printf.png)
<p class="img-caption">Figure 1: printf component.</p>

## Text size and color

It is possible to customize the size and color of the text produced by `cvui::printf()`. The following function signature can be used in that case:

```cpp
void printf (
    cv::Mat& theWhere,
    int theX,
    int theY,
    double theFontScale,
    unsigned int theColor,
    const char *theFmt,
    ...
);
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theFontScale` is the size of the text, `theColor` is the color of the text in the format `0xRRGGBB`, e.g. `0xff0000` for red, and `theFmt` is the formating string as it would be supplied for `stdio's printf()`, e.g. `"Text: %d and %f", 7, 3.1415`.

Below is an example of a text with customized size and color. Result on the screen is shown in Figure 2.

```cpp
double value = 3.14;
cvui::printf(frame, 90, 50, 0.8, 0x00ff00, "value = %.2f", value);
```

![printf with customized size and color]({{ site.url }}/img/printf-tweaked.png)
<p class="img-caption">Figure 2: text with customized size and color.</p>

## Learn more

Check the [main-app](https://github.com/Dovyski/cvui/tree/master/example/src/main-app) example for more information about <code>cvui::printf()</code>.
