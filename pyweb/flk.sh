#!/bin/sh

cd /Users/jade/workspace/python/pyweb
nodemon start_helloflask.py -w helloflask/__init__.py -w helloflask/templates/*.html
