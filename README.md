# asmr

source /var/www/html/django/.py3env/bin/activate

service httpd restart

python3 manage.py collectstatic

python3 manage.py runserver

