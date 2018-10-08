# Changelog
All notable changes to this project are documented in this file. The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## [2.7.0-BETA](https://github.com/Dovyski/cvui/releases/tag/v2.7.0-BETA) - 2018-06-26
### Added
- Python implementation of cvui, i.e. `cvui.py` ([read more](https://dovyski.github.io/cvui/usage/))
- [Python examples](https://github.com/Dovyski/cvui/tree/master/example/) ported from the already existing C++ ones.
- New [ui-enhanced-* examples](https://github.com/Dovyski/cvui/tree/master/example/), e.g. moving settings window ([#41](https://github.com/Dovyski/cvui/pull/41), [#36](https://github.com/Dovyski/cvui/pull/36), help from [Amaury Bréhéret](https://github.com/abreheret) and [ShengYu](https://github.com/shengyu7697)).
- Cmake option `ADD_PYTHON_EXAMPLES` to control the build of Python examples ([read more](https://dovyski.github.io/cvui/usage/)).

### Changed
- [Documentation](https://dovyski.github.io/cvui/) tweaks (help from [ShengYu](https://github.com/shengyu7697) and [Akash Kumar Singh](https://github.com/ksakash)).
- Cmake version `3.1` or higher is now required to build the examples.
- Cmake files were improved.
- `rect()` color filling now supports alpha values, e.g. `0x7700ff00` (green with 50% transparency) ([#39](https://github.com/Dovyski/cvui/pull/39), help from [Justin Muncaster](https://github.com/jmuncaster)).

### Fixed
- `rect()` issue related to opacity ([#42](https://github.com/Dovyski/cvui/pull/42), help from [Justin Muncaster](https://github.com/jmuncaster)).
- Conflict with `dirent.h` and `min()/max()` macros on Windows ([#38](https://github.com/Dovyski/cvui/issues/38), help from [Ali Zarei](https://github.com/AliZ-ee)).

## [2.5.0](https://github.com/Dovyski/cvui/releases/tag/v2.5.0) - 2018-04-04
### Added
- Support for [multiple windows](https://dovyski.github.io/cvui/advanced-multiple-windows/) (help from [Justin Muncaster](https://github.com/jmuncaster), [4xle](https://github.com/4xle) and Luca Del Tongo).
- [Mouse API](https://dovyski.github.io/cvui/advanced-mouse/) (help from [Pascal Thomet](https://github.com/pthom)).
- Compilation flag `CVUI_IMPLEMENTATION` ([read more](https://dovyski.github.io/cvui/usage/)).
- New parameter `bool theCreateNamedWindow` in `init()` ([read more](https://dovyski.github.io/cvui/advanced-multiple-windows/)).
- `init(const cv::String[], size_t, int, bool)` ([read more](https://dovyski.github.io/cvui/advanced-multiple-windows/)).
- `watch(cv::String, bool)` ([read more](https://dovyski.github.io/cvui/advanced-multiple-windows/)).
- `cvui::imshow()`, equivalent of calling `cvui::update()` then `cv::imshow()` ([read more](https://dovyski.github.io/cvui/advanced-multiple-windows/)).
- More [examples](https://github.com/Dovyski/cvui/tree/master/example/).
- Compilation flag `CVUI_DISABLE_COMPILATION_NOTICES` ([read more](https://dovyski.github.io/cvui/usage/)).

### Changed
- cvui can now be included in multiple files (help from Luca Del Tongo; [read more](https://dovyski.github.io/cvui/usage/)).
- Requirement that one (**and only one**) of your C++ files must include `cvui.h` after a `#define CVUI_IMPLEMENTATION` ([read more](https://dovyski.github.io/cvui/usage/)).
- [Documentation](https://dovyski.github.io/cvui/) was significantly improved, e.g. code samples, figures, etc.

### Fixed
- `sparkline()` crashes with empty vector ([#23](https://github.com/Dovyski/cvui/issues/23)).

## [2.0.0](https://github.com/Dovyski/cvui/releases/tag/v2.0.0) - 2017-05-24
### Added
- `image()`
- `iarea()`
- `trackbar()` component (thanks to [Pascal Thomet](https://github.com/pthom)).
- Support for OpenCV 2.x (thanks to [Pascal Thomet](https://github.com/pthom)).
- Basic cmake support for examples (thanks to [Pascal Thomet](https://github.com/pthom)).
- Multiplatform improvements (thanks to [ebachard](https://github.com/ebachard)).
- More [examples](https://github.com/Dovyski/cvui/tree/master/example/).
- Better [documentation](https://github.com/Dovyski/cvui/tree/master/docs/).

### Changed
- cvui is now a header-only lib.
- `button()` component can now use images.
- Labels in the `button()` component can have keyboard shortcuts with `&`, e.g. `&Quit` (thanks to [Pascal Thomet](https://github.com/pthom)).
- Fixes to README file (thanks to [Mateo Hrastnik](https://github.com/hrastnik)).

## [1.1.0](https://github.com/Dovyski/cvui/releases/tag/v1.1.0) - 2016-08-19
### Added
- `printf()`
- `rect()`
- `sparkline()`
- `space()`
- `begin*()` and `end*()` block.
- `cvui::VERSION`
- Docs for all components.
- More [examples](https://github.com/Dovyski/cvui/tree/master/example/).

## [1.0.0](https://github.com/Dovyski/cvui/releases/tag/v.1.0.0) - 2016-06-19
### Added
- `text()`
- `button()`
- `checkbox()`
- `window()`
- `counter()`
- Basic example app.
