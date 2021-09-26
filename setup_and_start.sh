#!/bin/sh

# Create env
python3 -m env .hex-ocean

# Use env
source ./.hex-ocean/bin/activate

# Install packages
pip3 install -r requirements.txt

# Setup db
python3 manage.py migrate

# Create uploads folder
mkdir uploads

# Run app
python3 manage.py runserver