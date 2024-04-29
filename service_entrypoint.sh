#!/bin/bash

sleep 5
flask db migrate
flask db upgrade
waitress-serve --port 5000 --call "${FLASK_APP}"

tail -f /dev/null