release: python video_download/manage.py migrate --noinput
web: cd video_download && gunicorn YoutubeVideoDownloader.wsgi 
worker: python3 video_download/run_pooling.py