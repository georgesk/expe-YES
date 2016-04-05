#!/bin/bash

ffserver -d -f ./ffserver.conf &

trap "killall ffserver && echo ffserver stopped; exit" SIGHUP SIGINT SIGTERM

ffmpeg -f video4linux2 -input_format mjpeg -s 160x120 -r 15 -i /dev/video0 http://localhost:8090/feed1.ffm
