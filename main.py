from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Config Flask
app = Flask(__name__)
app.secret_key = 'supersecret'

# Get DB credentials from environment variables
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_port = os.getenv('DB_PORT')
db_name = os.getenv('DB_NAME')

# Build the SQLAlchemy connection URI
db_uri = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Config upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Init DB
db = SQLAlchemy(app)

# Definim modelul generalizat
class Tranzactie(db.Model):
    __tablename__ = 'tranzactii'
    id = db.Column(db.Integer, primary_key=True)
    id_tranzactie = db.Column(db.String(100))
    sursa = db.Column(db.String(50))
    data_tranzactie = db.Column(db.Date)
    tip_tranzactie = db.Column(db.String(100))
    partener = db.Column(db.String(255))
    cui_partener = db.Column(db.String(50))
    valoare = db.Column(db.Float)
    valuta = db.Column(db.String(10))
    tva_percent = db.Column(db.Float)
    valoare_tva = db.Column(db.Float)
    cont_debitor = db.Column(db.String(50))
    cont_creditor = db.Column(db.String(50))
    descriere = db.Column(db.Text)
    status_plata = db.Column(db.String(50))
    tip_document = db.Column(db.String(50))
    categorie_financiara = db.Column(db.String(50))
    timestamp_import = db.Column(db.DateTime, default=datetime.utcnow)
    extra_data = db.Column(db.JSON)

# Creează tabelul dacă nu există
with app.app_context():
    db.create_all()

# Helper: detectăm și transformăm fișierele
def detect_and_transform(df):
    if 'Număr document' in df.columns:
        sursa = 'SmartBill'
        df_trans = pd.DataFrame()
        df_trans['id_tranzactie'] = None
        df_trans['sursa'] = sursa
        df_trans['data_tranzactie'] = pd.to_datetime(df['Data emiterii'], errors='coerce')
        df_trans['tip_tranzactie'] = df['Tip document']
        df_trans['partener'] = df['Nume client']
        df_trans['cui_partener'] = df.get('CIF client', '')
        df_trans['valoare'] = pd.to_numeric(df['Valoare totală'], errors='coerce')
        df_trans['valoare_tva'] = pd.to_numeric(df['Valoare TVA'], errors='coerce')
        df_trans['valuta'] = df.get('Valută', 'RON')
        df_trans['status_plata'] = df.get('Status plată', '')
        df_trans['descriere'] = df.get('Descriere', '')
        df_trans['tip_document'] = df['Tip document']
        df_trans['categorie_financiara'] = ''
        df_trans['cont_debitor'] = ''
        df_trans['cont_creditor'] = ''
        return df_trans, sursa

    elif 'Data tranzacție' in df.columns:
        sursa = 'Propriu'
        df_trans = pd.DataFrame()
        df_trans['id_tranzactie'] = None
        df_trans['sursa'] = sursa
        df_trans['data_tranzactie'] = pd.to_datetime(df['Data tranzacție'], errors='coerce')
        df_trans['tip_tranzactie'] = df['Tip tranzacție']
        df_trans['partener'] = df['Client/Furnizor']
        df_trans['cui_partener'] = ''
        df_trans['valoare'] = pd.to_numeric(df['Valoare'], errors='coerce')
        df_trans['tva_percent'] = pd.to_numeric(df['TVA (%)'], errors='coerce')
        df_trans['valoare_tva'] = (df_trans['valoare'] * (df_trans['tva_percent'] / 100)).round(2)
        df_trans['valuta'] = 'RON'
        df_trans['status_plata'] = ''
        df_trans['descriere'] = df.get('Detalii', '')
        df_trans['tip_document'] = df['Tip tranzacție']
        df_trans['categorie_financiara'] = df['Categorie']
        df_trans['cont_debitor'] = ''
        df_trans['cont_creditor'] = ''
        return df_trans, sursa

    else:
        raise ValueError("⚠️ Nu am putut detecta formatul fișierului!")

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file:
            flash('⚠️ Selectează un fișier CSV sau XLSX.')
            return redirect('/')

        filename = file.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(path)

        try:
            df = pd.read_csv(path) if filename.endswith('.csv') else pd.read_excel(path)
            df_trans, sursa = detect_and_transform(df)

            # Salvăm în DB
            for _, row in df_trans.iterrows():
                tranzactie = Tranzactie(
                    id_tranzactie=row.get('id_tranzactie'),
                    sursa=row.get('sursa'),
                    data_tranzactie=row.get('data_tranzactie'),
                    tip_tranzactie=row.get('tip_tranzactie'),
                    partener=row.get('partener'),
                    cui_partener=row.get('cui_partener'),
                    valoare=row.get('valoare'),
                    valuta=row.get('valuta'),
                    tva_percent=row.get('tva_percent'),
                    valoare_tva=row.get('valoare_tva'),
                    cont_debitor=row.get('cont_debitor'),
                    cont_creditor=row.get('cont_creditor'),
                    descriere=row.get('descriere'),
                    status_plata=row.get('status_plata'),
                    tip_document=row.get('tip_document'),
                    categorie_financiara=row.get('categorie_financiara'),
                    extra_data=json.loads(row.to_json())
                )
                db.session.add(tranzactie)
            db.session.commit()

            flash(f"✅ Fișier '{filename}' procesat și salvat cu succes ca sursă: {sursa}.")

        except Exception as e:
            flash(f"❌ Eroare la procesare: {e}")
        return redirect('/')

    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
