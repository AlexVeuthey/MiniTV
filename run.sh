#!/bin/bash
source `which virtualenvwrapper.sh`
workon minitv
git checkout stable && git pull
pip install -r requirements.txt
python -m minitv.app
deactivate
