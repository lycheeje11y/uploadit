#!/bin/bash

sleep 5
flask db migrate
flask db upgrade
waitress-serve --port 5000 --call 'uploadit:serve'

tail -f /dev/null