#!/bin/bash

sleep 5
flask db migrate
flask db upgrade
waitress-serve --port 5000 --host "0.0.0.0" --threads 20 --call "uploadit:runner"

tail -f /dev/null