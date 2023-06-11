bind = '192.168.50.13:5000'  # Specify the IP address and port to bind
workers = 4  # Number of worker processes
timeout = 120  # Timeout value in seconds

# application run command: gunicorn --config gunicorn_config.py app:app
