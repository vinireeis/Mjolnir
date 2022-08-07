# Mjolnir
from src.controllers.controller import app

# Third party
from asgiref.wsgi import WsgiToAsgi

asgi_app = WsgiToAsgi(app)
