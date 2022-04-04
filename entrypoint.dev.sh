#!/bin/sh
flask db migrate
flask run --port=8000 --host=0.0.0.0
