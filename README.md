# asmr

source /var/www/html/django/.py3env/bin/activate


vim /etc/httpd/conf.d/django.conf

source /etc/httpd/conf.d/django.conf

vim /etc/httpd/conf.d/httpd.conf

source /etc/httpd/conf.d/httpd.conf


service httpd restart

python3 manage.py collectstatic

python3 manage.py runserver

