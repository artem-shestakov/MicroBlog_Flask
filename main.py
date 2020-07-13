from flask import Flask
from config import DevConfig

# Init Flask application and app config
app = Flask(__name__)
app.config.from_object(DevConfig)


# Root route
@app.route("/")
def home():
    return "<h1>Hello world</h1>"


if __name__ == '__main__':
    app.run(host="0.0.0.0")
