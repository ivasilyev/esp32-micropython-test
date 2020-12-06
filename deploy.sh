#!/usr/bin/env bash

PORT=COM5

for FILE in __init__.py main.py config.json utils.py demo.py http_server.py index.html styles.css color_maps.py colors.py
  do
    echo Copy ${FILE}
    ampy --port ${PORT} --baud 115200 put ${FILE}
  done
