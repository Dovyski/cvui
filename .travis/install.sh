#!/bin/bash

if [[ $TRAVIS_OS_NAME == 'linux' ]]; then
	# OpenCV install code (modified from orignal source: https://github.com/jayrambhia/Install-OpenCV)

	#######################################################
	# Configuration variables
	#######################################################

	# Decide if some OpenCV extensions should be enabled or not for
	OPENCV_WITH_IPP=ON
	OPENCV_WITH_TBB=ON

	#######################################################
	# Install everything according to the configuration
	# variables above.
	#######################################################

	sudo apt-get install -y build-essential
	sudo apt-get install -y git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
	sudo apt-get install -y python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev

	curl -sL https://github.com/Itseez/opencv/archive/$OPENCV.zip > opencv.zip
	unzip -q opencv.zip

	cd opencv-$OPENCV

	# Create a new 'build' folder.
	mkdir build
	cd build

	if [[ $OPENCV == '3.0.0' ]]; then
		# Build fails if IPP is enabled when building OpenCV 3.0.0
		OPENCV_WITH_IPP=OFF
	fi

	# Set build instructions for Ubuntu distro.
	cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=$OPENCV_WITH_TBB -D WITH_IPP=$OPENCV_WITH_IPP -D BUILD_NEW_PYTHON_SUPPORT=OFF -D WITH_V4L=OFF -D INSTALL_C_EXAMPLES=OFF -D INSTALL_PYTHON_EXAMPLES=OFF -D BUILD_EXAMPLES=OFF -D WITH_QT=OFF -D WITH_OPENGL=OFF ..

	# Run 'make' with four threads.
	make -j4

	# Install to OS.
	sudo make install

	# Add configuration to OpenCV to tell it where the library files are located on the file system (/usr/local/lib)
	sudo sh -c 'echo "/usr/local/lib" > /etc/ld.so.conf.d/opencv.conf'

	sudo ldconfig
	echo "OpenCV installed."

	# We need to return to the repo "root" folder, so we can then 'cd' into the C++ project folder.
	cd ../../
fi
