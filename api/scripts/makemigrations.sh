#!/bin/bash
python3 manage.py makemigrations api_accounts &&
python3 manage.py makemigrations api_auth && 
python3 manage.py makemigrations api_clubs &&
python3 manage.py makemigrations api_events &&
python3 manage.py makemigrations api_roles &&
python3 manage.py makemigrations
