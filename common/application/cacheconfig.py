from flask_caching import Cache
from common.application.application import app

cache = Cache(app, config={'CACHE_TYPE': 'simple', 'CACHE_DEFAULT_TIMEOUT': 3600})  # Cache for 1 hour
