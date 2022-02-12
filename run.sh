#!/bin/bash
source `which virtualenvwrapper.sh`
workon minitv
# pip install -r requirements.txt
python -m minitv.app
deactivate
