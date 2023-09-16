import multiprocessing
import os

bind = os.getenv('WEB_BIND', "0.0.0.0:8000")
accesslog = '-'

# each core can handle 2 processes and + 1 for some
# extra process, for example request to DB
workers = multiprocessing.cpu_count() * 2 + 1

errorlog = os.path.join(os.path.dirname(__file__), '../logs/gunicorn_error.log')
accesslog = os.path.join(os.path.dirname(__file__), '../logs/gunicorn_access.log')

# Whether to send Django output to the error log
capture_output = True

# How verbose the Gunicorn error logs should be
loglevel = "info"
