#!/bin/bash
echo "from django.contrib.auth.models import User; User.objects.create_superuser(first_name='admin', last_name='last', username='admin', email='admin@mtgrecorder.com', password='password')" | python manage.py shell
