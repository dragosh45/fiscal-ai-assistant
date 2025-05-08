from flask import Flask
from config import Config
from models import db
from routes.upload_routes import upload_blueprint
from routes.api_routes import api_blueprint
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

app.register_blueprint(upload_blueprint)
app.register_blueprint(api_blueprint)

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)