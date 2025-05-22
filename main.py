from flask import Flask, redirect
from config import Config
from models import db
from flask_sqlalchemy import SQLAlchemy
import os

# Importă blueprint-urile
from routes.upload_file_routes import upload_bp
from routes.import_bancar_routes import bancar_bp
from routes.transform_efactura_routes import transform_bp
from routes.transform_efactura_to_xml_routes import transform_xml_bp

# Inițializare aplicație Flask
app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Înregistrează blueprints
app.register_blueprint(upload_bp)
app.register_blueprint(bancar_bp)
app.register_blueprint(transform_bp)
app.register_blueprint(transform_xml_bp)

# Creează folderul pentru uploads dacă nu există
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Creează tabelele la prima rulare (doar dacă nu există)
with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return redirect("/upload-file")


# Pornire aplicație în mod local
if __name__ == '__main__':
    app.run(debug=True)
