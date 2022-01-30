#!/bin/bash
source `which virtualenvwrapper.sh`
workon minitv
python -m minitv.app
