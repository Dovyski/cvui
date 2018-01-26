cmake_minimum_required(VERSION 2.8.12)
project( cvui )

# For cmake 2.8.12 and higher
if (NOT MSVC)
  add_compile_options(-std=c++11)
endif()

# New way for cmake 3.1 and higher
#set(CMAKE_CXX_STANDARD 11) # C++11...
#set(CMAKE_CXX_STANDARD_REQUIRED ON)
#set(CMAKE_CXX_EXTENSIONS OFF) #...without compiler extensions like gnu++11

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

# Copy all data files
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-gray.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-red.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/sparkline.csv DESTINATION ${CMAKE_BINARY_DIR}/bin/)

file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Debug)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Debug)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-gray.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Debug)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-red.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Debug)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/sparkline.csv DESTINATION ${CMAKE_BINARY_DIR}/bin/Debug)

file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Release)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Release)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-gray.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Release)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/lena-face-red.jpg DESTINATION ${CMAKE_BINARY_DIR}/bin/Release)
file(COPY ${CMAKE_SOURCE_DIR}/example/data/sparkline.csv DESTINATION ${CMAKE_BINARY_DIR}/bin/Release)
