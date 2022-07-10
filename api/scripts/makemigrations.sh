#!/bin/bash
python3 manage.py makemigrations api_accounts &&
python3 manage.py makemigrations api_auth && 
python3 manage.py makemigrations api_clubs &&
python3 manage.py makemigrations
