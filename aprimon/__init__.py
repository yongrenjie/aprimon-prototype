from flask import Flask

# This is actually a local package import
from config import Config
app = Flask(__name__)
app.config.from_object(Config)

# Put at the end to avoid circular dependencies
from aprimon import routes
