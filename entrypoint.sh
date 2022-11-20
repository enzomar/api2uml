#!/bin/bash

exec gunicorn --config gunicorn_config.py main:app