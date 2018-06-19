cmake_minimum_required(VERSION 3.1)
project(cvui LANGUAGES CXX)

# Option to control if python things should be included or not.
option(ADD_PYTHON_EXAMPLES "Add cvui.py (Python version of cvui) and Python examples to the build." ON)

set(CMAKE_CXX_STANDARD 11)           # C++11
set(CMAKE_CXX_STANDARD_REQUIRED OFF)
set(CMAKE_CXX_EXTENSIONS OFF)        # without compiler extensions like gnu++11

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin)

add_subdirectory(example/src/button-shortcut)
add_subdirectory(example/src/canny)
add_subdirectory(example/src/complext-layout)
add_subdirectory(example/src/hello-world)
add_subdirectory(example/src/image-button)
add_subdirectory(example/src/interaction-area)
add_subdirectory(example/src/main-app)
add_subdirectory(example/src/mouse)
add_subdirectory(example/src/mouse-complex)
add_subdirectory(example/src/mouse-complex-buttons)
add_subdirectory(example/src/multiple-files)
add_subdirectory(example/src/multiple-windows)
add_subdirectory(example/src/multiple-windows-complex)
add_subdirectory(example/src/multiple-windows-complex-dynamic)
add_subdirectory(example/src/multiple-windows-complex-mouse)
add_subdirectory(example/src/nested-rows-columns)
add_subdirectory(example/src/on-image)
add_subdirectory(example/src/row-column)
add_subdirectory(example/src/sparkline)
add_subdirectory(example/src/trackbar)
add_subdirectory(example/src/trackbar-complex)
add_subdirectory(example/src/trackbar-sparkline)
add_subdirectory(example/src/ui-enhanced-canny)
add_subdirectory(example/src/ui-enhanced-window-component)

# Copy all data files
message(STATUS "Copying data files")
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena.jpg DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face.jpg DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-gray.jpg DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-red.jpg DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
file(COPY ${CMAKE_SOURCE_DIR}/example/data/fruits.jpg DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
file(COPY ${CMAKE_SOURCE_DIR}/example/data/sparkline.csv DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
message(STATUS "Copying data files - done")

# Copy python stuff if that was requested
if(ADD_PYTHON_EXAMPLES)
	message(STATUS "Python examples will be added, e.g. cvui.py")
	file(COPY ${CMAKE_SOURCE_DIR}/cvui.py DESTINATION ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
endif()