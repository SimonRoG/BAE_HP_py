import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1

loglevel = 'info'
accesslog = 'gunicorn_access.log'
errorlog = 'gunicorn_error.log'