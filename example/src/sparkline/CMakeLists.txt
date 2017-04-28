find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
include_directories(../../..)

set(ApplicationName sparkline)

add_executable(${ApplicationName} main.cpp)
target_link_libraries( ${ApplicationName} ${OpenCV_LIBS} )
set_property(TARGET ${ApplicationName} PROPERTY CXX_STANDARD 11)
install(TARGETS ${ApplicationName} DESTINATION bin)
install(FILES ../../data/sparkline.csv DESTINATION bin)