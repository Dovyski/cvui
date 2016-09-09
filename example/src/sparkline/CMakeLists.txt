find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
include_directories(../../..)

set(ApplicationName sparkline)

add_executable(${ApplicationName} main.cpp ../../../cvui.cpp)
target_link_libraries( ${ApplicationName} ${OpenCV_LIBS} )
