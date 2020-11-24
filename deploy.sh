#!/usr/bin/env bash

PORT=COM5

for FILE in __init__.py main.py config.json utils.py demo.py http_server.py index.html
  do
    ampy --port ${PORT} --baud 115200 put ${FILE}
  done
