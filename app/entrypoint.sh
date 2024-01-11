#!/bin/sh

flask db upgrade
sleep 10
flask run --host=0.0.0.0

