---
layout: default
title: rect
---

# Rect

`cvui::rect()` renders a rectangle, filled or not. The signature of the function is:

{% highlight c++ %}
void rect (
    cv::Mat& theWhere,
    int theX,
    int theY,
    int theWidth,
    int theHeight,
    unsigned int theBorderColor,
    unsigned int theFillingColor = 0xff000000
)
{% endhighlight %}

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theWidth` is the width of the rectangle, `theHeight` is the height of the rectangle, `theBorderColor` is the color of rectangle's border in the format `0xRRGGBB`, e.g. `0xff0000` for red, and `theFillingColor` is the color of rectangle's filling in the format `0xAARRGGBB`, e.g. `0x00ff0000` for red, `0xff000000` for transparent filling.

Below is an example showing a rectangle with no filling color (transparent). The result on the screen is shown in Figure 1.

{% highlight c++ %}
cvui::rect(frame, 60, 10, 130, 90, 0xff0000);
{% endhighlight %}

![Rectangle with no filling](/img/rect.png)
<p class="img-caption">Figure 1: rect component.</p>

Rectangles can be filled with a solid color, as demonstrated below. Result on the screen shown in Figure 2.

{% highlight c++ %}
cvui::rect(frame, 60, 10, 130, 90, 0xff0000, 0x00ff00);
{% endhighlight %}

![Button](/img/rect-filled.png)
<p class="img-caption">Figure 2: rect component filled with a solid color.</p>

<div class="notice--warning">Currently it is not possible to define the transparency, i.e. alpha value different than <code>0xff000000</code>, for a rectangle's filling.</div>

## Learn more

Check the [complex-layout](https://github.com/Dovyski/cvui/tree/master/example/src/complex-layout) example for more information about rect.
