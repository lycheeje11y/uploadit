#!/bin/bash

echo "Starting Debug SMTP Server, Listening On address '127.0.0.1' and port '8025'"

aiosmtpd -n -c aiosmtpd.handlers.Debugging -l localhost:8025

echo "\nFinished Debug SMTP Server. Exiting"
