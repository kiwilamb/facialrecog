# facialrecog
Track and recognise the largest face from a webcam of video feed. Currently only tested on Ubuntu 16.04

## Install Dependencies
Install dlib, scikit-image and scipy:

    sudo apt-get install cmake, libboost-all-dev
    sudo pip3 install scikit-image, scipy, dlib

Install OpenCV, the following commands were based on these [instructions](http://docs.opencv.org/3.2.0/d7/d9f/tutorial_linux_install.html):

    sudo apt-get install build-essential
    sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
    sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev
    cd /srv
    git clone https://github.com/opencv/opencv.git
    cd opencv
    mkdir build
    cd build
    cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local -D PYTHON3_EXECUTABLE=/usr/bin/python3.5 -D PYTHON_INCLUDE_DIR=/usr/include/python3.5 -D PYTHON_INCLUDE_DIR2=/usr/include/x86_64-linux-gnu/python3.5m -D PYTHON_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.5m.so -D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/python3.5/dist-packages/numpy/core/include/ /srv/opencv
    make -j7
    sudo make install

Install OpenFace. Either use the [docker image](https://cmusatyalab.github.io/openface/setup/#with-docker) or [install manually](https://cmusatyalab.github.io/openface/setup/#by-hand). If you use the Docker image you'll need to have [Docker installed too](https://docs.docker.com/engine/installation/linux/ubuntulinux/#/install-the-latest-version)

## To Do
* Add unit tests using pytest
* Add ability to recognise faces using lua script from OpenFace
* Try to improve FPS by only recognising face once and tracking face movement once per second
* Try using optical flow from OpenCV to track face, does it improve FPS?
* Add a license
