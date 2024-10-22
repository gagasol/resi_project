#!/bin/bash

if [ -f ./.venv/bin/activate ]; then
    echo "Starting up virtuell env .."
    source .venv/bin/activate
    python main.py
else
    echo "installing missing module :"
    sudo zypper install libgthread-2_0-0 libgthread-2_0-0-32bit
    echo "Setting up virtuel env .."
    python3.12 -m venv .venv
    source .venv/bin/activate
    echo "Installing requirements .."
    python -m pip install -r requirements.txt
    echo "Starting application .."
    python main.py
fi
deactivate