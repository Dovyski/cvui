---
layout: default
title: index
---

# cvui

cvui is a (very) simple UI lib built on top of OpenCV drawing primitives. Other UI libs, such as [imgui](https://github.com/ocornut/imgui), require a graphical backend (e.g. OpenGL) to work, so if you want to use imgui in a OpenCV app, you must make it OpenGL enabled, for instance.

It is not the case with cvui, which uses *only* OpenCV drawing primitives to do all the rendering (no OpenGL or Qt required).

![image](https://raw.githubusercontent.com/Dovyski/depository/master/cvui.png?20171201)

## Features

- Lightweight and simple to use user interface;
- Header-only with no external dependencies (except OpenCV);
- Based on OpenCV drawing primitives only (OpenGL or Qt are not required);
- Friendly and C-like API (no classes/objects, etc);
- Easily render components without worrying about their position (using rows/columns);
- Simple (yet powerful) mouse API;
- Modest number of UI components (11 in total);
- Available in C++ and Python (pure implementation, no bindings).
