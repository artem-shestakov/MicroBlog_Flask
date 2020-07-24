import os
from wedapp import create_app

# Get config Class for app and create app
env = os.environ.get("WEBAPP_ENV", "dev")
app = create_app(f"config.{env.capitalize()}Config")

if __name__ == '__main__':
    app.run(host="0.0.0.0")
