#!/usr/bin/env bash

# ampy --port COM5 --baud 115200 get "boot.py" "boot.py"
for FILE in __init__.py main.py config.json utils.py demo.py http_server.py index.html styles.css color_maps.py colors.py
  do
    echo Copy ${FILE}
    ampy put ${FILE}
  done
