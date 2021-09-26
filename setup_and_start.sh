#!/bin/sh

# Create env
python3 -m venv .hex

# Use env
source ./.hex/bin/activate

# Install packages
pip3 install -r requirements.txt

# Setup db
python3 manage.py migrate

# Create uploads folder
mkdir uploads

# Run app
python3 manage.py runserver