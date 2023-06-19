from flask import Flask
from flask_cors import CORS

# Initialize Flask Application
app = Flask(__name__)

# Set the CORS * to accept any request
CORS(app, origins=['*'])
