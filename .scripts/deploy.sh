# #!/bin/bash
# set -e

# echo " ----  Code By Kuldeepsaini65  ----- "
# echo "Deployment started ..."

# # Pull the latest version of the app
# git pull
# echo "New changes copied to server !"

# # Activate Virtual Env
# #source ~/project/venv/bin/activate
# #echo "Virtual env 'venv' Activated !"

# echo "Installing Dependencies..."
# pip install -r requirements.txt --no-input

# echo "Serving Static Files..."
# python manage.py collectstatic --noinput

# echo "Running Database migrations..."
# python manage.py makemigrations
# python manage.py migrate

# # Deactivate Virtual Env
# deactivate
# echo "Virtual env 'venv' Deactivated !"

# # Reloading Application So New Changes could reflect on website
# cd ~/project/javagurukul
# touch wsgi.py
# cd -

# systemctl restart gunicorn
# echo "******Restarted Gunicron*****"
# systemctl restart nginx
# echo "******Restarted Nginx*****"

# echo "Deployment Finished!"

# echo "Happy Coding...."
