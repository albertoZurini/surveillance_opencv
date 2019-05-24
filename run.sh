#!/bin/bash

# xhost +

CMD=bash
#python3 main.py

nvidia-docker run --rm -it \
--device=/dev/nvidiactl \
--device=/dev/nvidia-uvm \
--device=/dev/nvidia0 \
-v nvidia_driver_384.66:/usr/local/nvidia:ro \
--env DISPLAY=unix$DISPLAY  \
--privileged --volume $XAUTH:/root/.Xauthority \
--volume /tmp/.X11-unix:/tmp/.X11-unix \
-v $PWD/script:/script \
--name surveillance_gpu surveillance_gpu $CMD

