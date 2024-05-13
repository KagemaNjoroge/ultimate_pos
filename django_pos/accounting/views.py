from django.shortcuts import render

import django_pos

# Create your views here.


def index(request):
    return render(request, "accounting/index.html")






# [Unit]
# Description=gunicorn daemon
# Requires=gunicorn.socket
# After=network.target

# [Service]
# User=Njoroge
# Group=www-data
# WorkingDirectory=/home/Njoroge/ultimate_pos/django_pos
# ExecStart=/home/Njoroge/ultimate_pos/django_pos/venv/bin/gunicorn \
#           --access-logfile - \
#           --workers 3 \
#           --bind unix:/run/gunicorn.sock \
#           django_pos.wsgi:application

# [Install]
# WantedBy=multi-user.target