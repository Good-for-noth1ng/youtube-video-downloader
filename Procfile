release: python video_download/manage.py migrate --noinput
web: gunicorn gettingstarted.wsgi 
worker: python3 video_download/run_pooling.py