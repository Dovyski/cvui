---
layout: default
title: advanced-introduction
---

# Mouse and OpenCV windows
Some applications require more complex UI interactions, including the use of the mouse cursor or multiple OpenCV windows.

The only thing you need to consider when using multiple OpenCV windows (containing cvui components) or cvui's mouse API is that **cvui must be informed about the window it is opperating**. That way cvui can correctly perform its calculations, e.g. clicks, using the right window space.

<div class="notice--info">All cvui functions are context aware, so they will try as best as possible to guess which on window they are working.</div>

## Mouse
cvui has its own mouse API which facilitates the tracking of mouse clicks and cursor position. Check out the [mouse page](/advanced-mouse) to learn more.

## Multiple OpenCV windows with cvui compoments
If your application uses multiple OpenCV windows (via `cv::imshow()`) and at least two of them use cvui compoments, you need some additional (yet simple) configuration. Check out the [multiple windows page](/advanced-multiple-windows) to learn more.
