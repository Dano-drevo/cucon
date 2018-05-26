#!/bin/bash
#This is a sample configuration. Go with it or choose your own.
PORT=4000
HOST=127.0.0.1
#It is recommended to have (<number of CPU*2)+1 cores> workers.
#In this case, we chose to have only one worker per available CPU:
WORKERS=$(nproc)

gunicorn -w $WORKERS -b "$HOST:$PORT" --log-level=debug --preload --timeout 10 run:app

