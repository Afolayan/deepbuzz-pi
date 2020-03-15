#!/usr/bin/env bash

cd /home/pi/deepbuzz-pi
source venv/bin/activate &
flask run --host 0.0.0.0 &
sudo python3 location.py &
sudo python3 signalr_commands.py