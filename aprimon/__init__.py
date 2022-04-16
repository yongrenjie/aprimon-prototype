from flask import Flask

app = Flask(__name__)

# Put at the end to avoid circular dependencies
from aprimon import routes
