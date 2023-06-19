from config.env import getEnv
bind = '{}:{}'.format(getEnv('SERVER_ADDRESS'),getEnv('APP_PORT'))  # Specify the IP address and port to bind
workers = 4  # Number of worker processes
timeout = 120  # Timeout value in seconds

# application run command: gunicorn --config gunicorn_config.py app:app
