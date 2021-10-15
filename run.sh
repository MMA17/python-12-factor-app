#!/bin/bash

python3 ./httpserver.py &

python3 ./__init__.py &

exit $?