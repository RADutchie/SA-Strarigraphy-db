#!/bin/sh

exec gunicorn --config gunicorn_config.py manage:app
