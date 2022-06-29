release: python video_download/manage.py migrate --noinput
web: gunicorn video_download.wsgi
worker: python3 video_download/run_pooling.py