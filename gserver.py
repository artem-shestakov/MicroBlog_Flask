from gevent import monkey; monkey.patch_all()

from gevent.pywsgi import WSGIServer
from webapp import create_app
from webapp.cli import register

# Create app object
app = create_app("config.DevConfig")
register(app)

# Run Gevent server
if __name__ == '__main__':
    http_server = WSGIServer(('0.0.0.0', 3000), app)
    http_server.serve_forever()
