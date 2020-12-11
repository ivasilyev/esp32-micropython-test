#!/usr/bin/env bash

# ampy --port COM5 --baud 115200 get "boot.py" "boot.py"
for FILE in boot.py utils.py config.json \
  __init__.py main.py demo.py http_server.py index.html styles.css main.js
  do
    echo Copy ${FILE}
    ampy put ${FILE}
  done
