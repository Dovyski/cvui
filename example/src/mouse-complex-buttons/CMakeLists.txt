find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
include_directories(../../..)

set(ApplicationName mouse-complex-buttons)

add_executable(${ApplicationName} main.cpp)
target_link_libraries( ${ApplicationName} ${OpenCV_LIBS} )
set_property(TARGET ${ApplicationName} PROPERTY CXX_STANDARD 11)
install(TARGETS ${ApplicationName} DESTINATION bin)
install(FILES ../../data/lena.jpg DESTINATION bin)

if(ADD_PYTHON_EXAMPLES)
	add_custom_command(
        TARGET ${ApplicationName}
		POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/*.py ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}
	)
endif()
