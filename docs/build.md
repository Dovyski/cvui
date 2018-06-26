---
layout: default
title: build
---

# Build

cvui **does not require any build procedure**. Just add the `cvui.h` (or `cvui.py`) file along with the rest of your source code and continue to compile/run your project the way you have being doing so far.

cvui has no dependency other than OpenCV `3.x` (or `2.x`) itself. Check the [usage page]({{ site.url }}/usage) to learn how to use cvui.

## Building the examples

The [examples](https://github.com/Dovyski/cvui/tree/master/example) provided with the lib do require a build. You can use [cmake](https://cmake.org) to build them.
First clone cvui git repo:

```
git clone https://github.com/Dovyski/cvui.git cvui && cd cvui
```

Let's start with a __release build__. Create a folder to house the release files:

```
mkdir build.release && cd build.release
```

Generate project files:

```
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=g++ -DADD_PYTHON_EXAMPLES=ON
```

Build everything:

```
make -j4
```

Now for the __debug build__, go to the folder where cvui was cloned to:

```
cd ..
```

Create the folder to house the debug files:

```
mkdir build.debug && cd build.debug
```

Generate project files:

```
cmake .. -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=g++ -DADD_PYTHON_EXAMPLES=ON
```

Build everything:

```
make -j4
```

## cvui.py and Python examples

By default, cmake will add `cvui.py` (Python port of cvui) and the Python examples to the build folder. If you don't want Python files, use `-DADD_PYTHON_EXAMPLES=OFF` in the cmake commands, e.g:

```
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=g++ -DADD_PYTHON_EXAMPLES=OFF
```
