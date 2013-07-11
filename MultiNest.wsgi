import sys
# Path to the MultiNest module
sys.path.insert(0, "/var/www/wsgi/AppMultiNest")

# WSGI entry point
from MultiNest import app as application

