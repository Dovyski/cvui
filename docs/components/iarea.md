---
layout: default
title: iarea
---

# iarea

`cvui::iarea()` creates an interaction area that reports mouse cursor activity. The signature of the function is:

```cpp
int iarea(int theX, int theY, int theWidth, int theHeight);
```

where `theX` is the position X, `theY` is the position Y, `theWidth` is the width of the interaction area, and `theHeight` is the height of the interaction area.

`cvui::iarea()` returns the tracked interaction within the defined boundaries. Possible returns are:
* `cvui::OUT`: when the mouse cursor is not over the iarea.
* `cvui::OVER`: when the mouse cursor is over the iarea.
* `cvui::DOWN`: when the mouse cursor is pressed over the iarea, but not released yet.
* `cvui::CLICK`: when the mouse cursor clicked (pressed and released) within the iarea.

<div class="notice--info"><strong>IMPORTANT:</strong> <code>cvui::iarea()</code> does not produce any visual output on the screen. It is intended to be used as an auxiliary tool to create interactions.</div>

Below is an example showing an interaction area and its interaction with the mouse cursor.

```cpp
int status = cvui::iarea(30, 70, 90, 100);

// render a rectangle in the iarea, so we can see it
cvui::rect(30, 70, 90, 100);

switch (status) {
  case cvui::CLICK:  std::cout << "Clicked!" << std::endl; break;
  case cvui::DOWN:   cvui::printf(frame, 240, 70, "Mouse is: DOWN"); break;
  case cvui::OVER:   cvui::printf(frame, 240, 70, "Mouse is: OVER"); break;
  case cvui::OUT:    cvui::printf(frame, 240, 70, "Mouse is: OUT"); break;
}
```

![iarea]({{ site.url }}/img/iarea.gif)
<p class="img-caption">Figure 1: tracked interaction within an interaction area (iarea).</p>

## Learn more

Check the [interaction-area](https://github.com/Dovyski/cvui/tree/master/example/src/interaction-area) example for more information about iarea.
