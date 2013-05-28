To install all dependencies (I recommend a virtualenv):

pip install -r requirements.txt

Do usual Django-stuff, then edit conf.py and change BASE_BLOG_PATH,
BASE_OUTPUT_PATH, URL_SUFFIX (at least).

To start a worker:

python manage.py rqworker default

To start the test server:

python manage.py runserver
