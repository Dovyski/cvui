---
layout: default
title: advanced-mouse
---

# Mouse

cvui has its own mouse API to track mouse clicks and cursor position, for instance. Everything related to the mouse can be accessed from `cvui::mouse()`. The following sections will detail all mouse information available.

## Cursor position

You can query the position of the mouse cursor any moment by calling `cvui::mouse()`, which returns a `cv::Point`:

```cpp
cv::Point mouse(const cv::String& theWindowName = "")
```

Usage example:

```cpp
// Save the mouse cursor to a point object
cv::Point cursor = cvui::mouse();
std::cout << "x: " << cursor.x << " y: " << cursor.y << std::endl;

// or access the position directly
std::cout << "x: " << cvui::mouse().x << " y: " << cvui::mouse().y << std::endl;
```

Calls to `cvui::mouse()` follow the cvui philosophy of always returning current information, so you don't have to listen to mouse events, for instance. Just call `cvui::mouse()` and you get the most up-to-date position of the mouse cursor.

## Detect events, e.g. clicks

You can query the state of the mouse, e.g. clicks, by calling `cvui::mouse(int)`, whose signature is:

```cpp
bool mouse(int theQuery)
```

The parameter `theQuery` is an integer that specifies your query. Available queries are:

* `cvui::DOWN`: query if *any* mouse button was pressed. `cvui::mouse()` returns `true` for a single frame only (the one a mouse button went down).
* `cvui::UP`: query if *any* mouse button was released. `cvui::mouse()` returns `true` for a single frame only (the one a mouse button went up).
* `cvui::CLICK`: query if *any* mouse button was clicked (went down then up, no matter the amount of frames in between). `cvui::mouse()` returns `true` for a single frame only.
* `cvui::IS_DOWN`: query if *any* mouse button is currently pressed. `cvui::mouse()` returns `true` for as long as the button is down/pressed.

<div class="notice--info"><strong>IMPORTANT:</strong> calls to <code>cvui::mouse(int)</code> will query all mouse buttons, so the call <code>cvui::mouse(cvui::DOWN)</code> will return <code>true</code> if <strong>any</strong> mouse button was pressed.</div>

Below is an example that shows a message when any mouse button is pressed:

```cpp
if (cvui::mouse(cvui::DOWN)) {
	std::cout << "Any mouse button just went down." << std::endl;
}
```

Below is an example that shows a message only when any mouse button is clicked (pressed then released):

```cpp
if (cvui::mouse(cvui::CLICK)) {
	std::cout << "A mouse click just happened." << std::endl;
}
```

## Check mouse buttons individually

You can also query the state of a particular mouse button, e.g. react to clicks on the left button of the mouse.

Specific mouse buttons can be queried via `cvui::mouse(int, int)`, whose signature is:

```cpp
bool mouse(int theButton, int theQuery)
```

The parameter `theButton` allows you to specify which mouse button you want to query. Available buttons are `cvui::LEFT_BUTTON`, `cvui::MIDDLE_BUTTON` and `cvui::RIGHT_BUTTON`.

The function `cvui::mouse(int theButton, int theQuery)` works exactly as `cvui::mouse(int theQuery)` does, the only difference is that queries are target at a particular button, not all buttons.

Below is an example that prints a message when the left mouse button is pressed:

```cpp
if (cvui::mouse(cvui::LEFT_BUTTON, cvui::DOWN)) {
	std::cout << "Left mouse button just went down." << std::endl;
}
```

Here is another example that shows a message only when the left mouse button is clicked (pressed then released):

```cpp
if (cvui::mouse(cvui::LEFT_BUTTON, cvui::CLICK)) {
	std::cout << "Left mouse button click just happened." << std::endl;
}
```

## Learn more

Check out the [mouse](https://github.com/Dovyski/cvui/tree/master/example/src/mouse), [mouse-complex](https://github.com/Dovyski/cvui/tree/master/example/src/mouse-complex) and [mouse-complex-buttons](https://github.com/Dovyski/cvui/tree/master/example/src/mouse-complex-buttons) examples for more information about cvui's mouse API.
