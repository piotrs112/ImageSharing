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
mkdir uploads/200
mkdir uploads/400

# Create superuser
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('test_user', '', 'test_password')" |   python3 manage.py shell_plus

# Run app
python3 manage.py runserver