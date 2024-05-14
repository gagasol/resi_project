#!/bin/bash

if [ -f ./.venv/bin/activate ]; then
    echo "Starting up virtuell env .."
    source .venv/bin/activate
    python main.py
else
    PYV=$(python --version 2>&1)
    if [[ $PYV = *"3.12.3" ]]; then
        echo "Setting up virtuell env .."
        python3.12 -m venv .venv
        source .venv/bin/activate
        echo "Installing requirements .."
        python -m pip install -r requirements.txt
        echo "Starting application .."
        python main.py
    else
        echo "$PYV is the wrong version of python, please us 3.12.3 for this application"
        echo "use sudo zypper install python312 to get the package and rerun this script"
        echo "instead of zypper any other packet manager is usebale obviously"
        echo "If you have issues please check the README.txt or contact someone for help"
    fi

fi
