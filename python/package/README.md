# cvui

A (very) simple UI lib built on top of OpenCV drawing primitives. Other UI libs, such as [imgui](https://github.com/ocornut/imgui), require a graphical backend (e.g. OpenGL) to work, so if you want to use imgui in a OpenCV app, you must make it OpenGL enabled, for instance. It is not the case with cvui, which uses *only* OpenCV drawing primitives to do all the rendering (no OpenGL or Qt required).

![image](https://raw.githubusercontent.com/Dovyski/depository/master/cvui.png?20180627)

## Features

- Lightweight and simple to use user interface;
- Header-only with no external dependencies (except OpenCV);
- Based on OpenCV drawing primitives only (OpenGL or Qt are not required);
- Friendly and C-like API (no classes/objects, etc);
- Easily render components without worrying about their position (using rows/columns);
- Simple (yet powerful) mouse API;
- Modest number of UI components (11 in total);
- Available in C++ and Python (pure implementation, no bindings).

## Usage

Use of cvui revolves around calling `cvui.init()` to initialize the lib, rendering cvui components to a `np.ndarray` (that you handle yourself) and finally showing that `np.ndarray` on the screen using `cvui.imshow()`, which is cvui's version of `cv2.imshow()`. Alternatively you can use `cv2.imshow()` to show things, but in such case you must call `cvui.update()` yourself before calling `cv.imshow()`.

Below is an example:

```python
import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Test'

# Initialize cvui and create/open a OpenCV window.
cvui.init(WINDOW_NAME)
# Create a frame to render components to.
frame = np.zeros((200, 400, 3), np.uint8)

while True:
    # Clear the frame.
    frame[:] = (49, 52, 49)
    # Render a message in the frame at position (10, 15)
    cvui.text(frame, 10, 15, 'Hello world!')
    # Show frame in a window.
    cvui.imshow(WINDOW1_NAME, frame)

    if cv2.waitKey(20) == 27:
        break
```

The following sections explain in detail each one of the steps required to use cvui.

### 1. Import and initialize cvui

Before using cvui, you need to call `cvui.init()` to initialize it. The easiest way is to initialize cvui and tell it to create any OpenCV window that will be used, e.g.:

```python
import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Test'

# Tell cvui to init and create a window
cvui.init(WINDOW_NAME)

while True:
    # your app logic here
    if cv2.waitKey(20) == 27:
        break
```

**Tip:** if you need to use cvui with multiple windows, or you want more control over the process of creating windows, check the <a href="https://dovyski.github.io/cvui/advanced-multiple-windows">Multiple OpenCV windows</a> page and the <a href="https://github.com/Dovyski/cvui/tree/master/example/src/multiple-windows">multiple-windows</a> and <a href="https://github.com/Dovyski/cvui/tree/master/example/src/multiple-windows-complex">multiple-windows-complex</a> examples.</div>

### 2. Rendering and using cvui components

All cvui components are rendered to a `np.ndarray`. Below is an example showing how to render a `'Hello world'` message on a `np.ndarray` named `frame`:

```python
import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Test'

cvui.init(WINDOW_NAME)

# Create a frame
frame = np.zeros((200, 400, 3), np.uint8)

while True:
    # clear the frame
    frame[:] = (49, 52, 49)

    # render a message in the frame at position (10, 15)
    cvui.text(frame, 10, 15, 'Hello world!')

    if cv2.waitKey(20) == 27:
        break
```

Some cvui components, i.e. <a href="https://dovyski.github.io/cvui/components/counter/">counter</a>, <a href="https://dovyski.github.io/cvui/components/trackbar/">trackbar</a> and <a href="https://dovyski.github.io/cvui/components/checkbox/">checkbox</a>.</div>, use an external variable that they need to modify to control their internal state. Since there are no pointers to built-in types in Python, cvui components that need to change an external variable must receive such variable as an array/list with a single element.

Below is an example of a checkbox whose state is stored in the variable `checkboxState`:

```python
import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Test'
cvui.init(WINDOW_NAME)
frame = np.zeros((200, 400, 3), np.uint8)

# use an array/list because this variable will be changed by cvui
checkboxState = [False]

while True:
    frame[:] = (49, 52, 49)

    # Render the checkbox. Notice that checkboxState is used AS IS,
    # e.g. simply "checkboxState" instead of "checkboxState[0]".
    # Only internally that cvui will use checkboxState[0].
    cvui.checkbox(frame, 10, 15, 'My checkbox', checkboxState)

    # Check the state of the checkbox. Here you need to remember to
    # use the first position of the array/list because that's the
    # one being used by all cvui components that perform changes
    # to external variables.
    if checkboxState[0] == True:
        print('Checkbox is checked')

    if cv2.waitKey(20) == 27:
        break
```

**Tip:** see the <a href="https://dovyski.github.io/cvui/">online documentation</a> to learn more about all available cvui components.

### 3. Show (window) content

After rendering your components, show the final result using `cvui.imshow()`, which is cvui's improved version of OpenCV's `cv2.imshow()`:

```python
import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Test'

cvui.init(WINDOW_NAME)
frame = np.zeros((200, 400, 3), np.uint8)

while True:
    frame[:] = (49, 52, 49)
    cvui.text(frame, 10, 15, 'Hello world!')

    # Show window content
    cvui.imshow(WINDOW1_NAME, frame)

    if cv2.waitKey(20) == 27:
        break
```

When you use `cvui.imshow()` instead of `cv2.imshow()`, cvui will not only show the content, but update its internal structures to ensure all UI interactions work.

If you want to use `cv2.imshow()`, you must call `cvui.update()` before `cv2.imshow()` and after you are finished invoking cvui components, so cvui can perform its internal processing to handle mouse interactions. E.g.

```python
import numpy as np
import cv2
import cvui

WINDOW_NAME = 'CVUI Test'

cvui.init(WINDOW_NAME)
frame = np.zeros((200, 400, 3), np.uint8)

while True:
    frame[:] = (49, 52, 49)
    cvui.text(frame, 10, 15, 'Hello world!')

    # Update cvui internal stuff
    cvui.update()

    # Show window content
    cv2.imshow(WINDOW1_NAME, frame)

    if cv2.waitKey(20) == 27:
        break
```
