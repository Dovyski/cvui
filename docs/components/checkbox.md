---
layout: default
title: checkbox
---

# Checkbox

`cvui::checkbox()` renders a checkbox. The signature of the function is:

{% highlight c++ %}
bool checkbox (
    cv::Mat& theWhere,
    int theX,
    int theY,
    const cv::String& theLabel,
    bool *theState,
    unsigned int theColor = 0xCECECE
)
{% endhighlight %}

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, `theLabel` is text displayed besides the clickable checkbox square, `theState` describes the current state of the checkbox (`true` means the checkbox is checked) and `theColor` is color of the label in the format `0xRRGGBB`, e.g. `0xff0000` for red.

`cvui::checkbox()` returns a boolean value that indicates the current state of the checkbox: `true` if it is checked, or `false` otherwise.

Below is an example showing a checkbox. The result on the screen is shown in Figure 1.

{% highlight c++ %}
bool checked = false;
cvui::checkbox(frame, 80, 30, "Checkbox label", &checked);
{% endhighlight %}

![Button](/img/checkbox.png)
<p class="img-caption">Figure 1: checkbox component.</p>

## Learn more

Check the [main-app](https://github.com/Dovyski/cvui/tree/master/example/src/main-app) example for more information about checkbox.
