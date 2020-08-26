import os
from webapp import create_app
from webapp.cli import register

# Get config Class for app and create app
env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app(f"config.{env.capitalize()}Config")
register(app)
