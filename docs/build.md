---
layout: default
permalink: /build
id: build
---

# Build

cvui requires *no special build* procedures. Just add the `cvui.h` file along with the rest of your source code and continue to compile your project the way you have being do so far. cvui has no other dependency than OpenCV `3.x` (or `2.x`) itself.

The [examples](https://github.com/Dovyski/cvui/tree/master/example) provided with the lib do require a build. You can use cmake to build them.
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
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_COMPILER=gcc
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
cmake .. -DCMAKE_BUILD_TYPE=Debug -DCMAKE_CXX_COMPILER=gcc
```

Build everything:

```
make -j4
```
