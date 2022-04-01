#!/bin/sh
flask db migrate
flask run --host=0.0.0.0
