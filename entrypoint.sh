#!/bin/bash

exec gunicorn --config gunicorn_config.py api2umlweb:app