#!/bin/bash

#export MOTHERDUCK_TOKEN=...
export XDG_RUNTIME_DIR="/run/user/1000"
export PYTHON_PATH=./.venv/bin
$PYTHON_PATH/python ./quack.py ./media/quack.mp3 >> ./quack.log

