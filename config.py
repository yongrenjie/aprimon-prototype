import os

# eh, this isn't really being used
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "togekiss"
