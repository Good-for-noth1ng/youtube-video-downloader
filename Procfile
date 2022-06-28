release: python video_download/manage.py migrate --noinput
web: gunicorn YoutubeVideoDownloader.wsgi 
worker: python3 video_download/run_pooling.py