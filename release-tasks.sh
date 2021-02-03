#!/bin/bash

echo "Running Release Tasks"

#./manage.py makemigrations
./manage.py migrate
#./manage.py loaddata appdata.json
