---
layout: default
title: image
---

# Image

`cvui::image()` renders an image, i.e. `cv::Mat`. The signature of the function is:

```cpp
void image(cv::Mat& theWhere, int theX, int theY, cv::Mat& theImage);
```

where `theWhere` is the image/frame where the image will be rendered, `theX` is the position X, `theY` is the position Y, and `theImage` is an image to be rendered in the specified destination.

Below is an example showing an image being loaded then displayed using `cvui::image()`. The result on the screen is shown in Figure 1.

```cpp
cv::Mat lena_face = cv::imread("lena_face.jpg", cv::IMREAD_COLOR);
cvui::image(frame, 10, 10, lena_face);
```

![Image]({{ site.url }}/img/image.png)
<p class="img-caption">Figure 1: image <code>lena_face.jpg</code> displayed on the screen.</p>

## Learn more

Check the [image-button](https://github.com/Dovyski/cvui/tree/master/example/src/image-button) example for more information about images and buttons.
