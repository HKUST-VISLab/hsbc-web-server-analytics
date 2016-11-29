from flask import Flask
from flask_cors import CORS
app = Flask(__name__)
# flask_cors: Cross Origin Resource Sharing (CORS), making cross-origin AJAX possible.
app.config['DEBUG'] = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
CORS(app)
from app.routes import index

