release: python video_download/manage.py migrate --run-syncdb
release: python video_download/manage.py makemigrations
web: python3 video_download/run_pooling.py 
worker: python3 video_download/run_pooling.py