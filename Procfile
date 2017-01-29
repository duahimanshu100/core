web:python manage.py runserver
web: gunicorn analytics.wsgi --log-file -
heroku ps:scale web=1
