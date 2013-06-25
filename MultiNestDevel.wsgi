# WSGI entry point to AppGateway

# Setup PYTHONPATH for imports to work
import sys
sys.path.insert(0, "/var/www/wsgi/AppMultiNestDevel")

# Setup flask app as application to run by WSGI
from MultiNest import app as application

# Load the MultiNest configuration
from MultiNest import Config
Config.conf.load("/var/www/wsgi/AppMultiNestDevel/AppMultiNestDevel.json")
