#!/bin/bash

if [ -f ./venv/bin/activate ]; then
	echo "Starting up virtuell env .."
	source .venv/bin/activate
	echo "Starting application .."
	python main.py
else
	PYV=$(python --version 2>&1)
	if [[ $PYV = *"3.12" ]]; then
		echo "Initializing virtuell env .."
		python -m venv .venv
		source .venv/bin/activate
		python -m pip install -r requirements.txt
		python main.py
	else
		echo "$PYV is the wrong version of python, please us 3.12.x for this application"
		echo "If you have issues please check the README.txt or contact some help"