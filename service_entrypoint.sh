#!/bin/bash

sleep 5
flask db migrate
flask db upgrade
# waitress-serve --port 5000 --call 'uploadit:serve'
flask --app=uploadit:serve run --debug --host="0.0.0.0"

tail -f /dev/null