from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

client = app.test_client()

from app import routes
