#!/bin/sh 

start-stop-daemon --background --start --exec /usr/bin/Xvfb -- :8412 -screen 0 1024x768x16 -ac