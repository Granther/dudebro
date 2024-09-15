import os

workers = 2

threads = 4

# timeout = int(os.environ.get('GUNICORN_TIMEOUT', '120'))

bind = '0.0.0.0:5005'


forwarded_allow_ips = '*'

secure_scheme_headers = { 'X-Forwarded-Proto': 'https' }