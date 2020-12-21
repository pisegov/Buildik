#!/bin/bash

cd buildik-ui
npm run build
cd ..
python manage.py collectstatic  --noinput
python manage.py runserver
