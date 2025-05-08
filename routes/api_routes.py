from flask import Blueprint, jsonify, flash, redirect, url_for
from models import db, Tranzactie
from datetime import datetime
import requests
import hashlib  # adăugat pentru fallback id_tranzactie
import os, json

api_blueprint = Blueprint('api_routes', __name__)


@api_blueprint.route('/api/bancar', methods=['GET'])
def api_bancar_demo():
    file_path = os.path.join('uploads', 'bancar_mock_all.json')
    with open(file_path, encoding='utf-8') as f:
        data = json.load(f)
    return jsonify(data)


@api_blueprint.route('/import-bancar')
def import_bancar():
    try:
        response = requests.get("http://localhost:5000/api/bancar")
        response.raise_for_status()
        data = response.json()

        for entry in data:
            id_tranzactie = entry.get("id_tranzactie")

            # Dacă ID-ul este lipsă sau invalid (None, NaN), generează fallback ID
            if not id_tranzactie or str(id_tranzactie).lower() == 'nan':
                key = f"{entry.get('data')}_{entry.get('valoare')}_{entry.get('partener')}_{entry.get('tip')}"
                id_tranzactie = hashlib.sha1(key.encode()).hexdigest()

            # Verifică dacă deja există
            existing = Tranzactie.query.filter_by(id_tranzactie=id_tranzactie).first()
            if existing:
                continue  # Sărim peste duplicate

            tranzactie = Tranzactie(
                id_tranzactie=id_tranzactie,
                sursa='API bancar',
                data_tranzactie=datetime.strptime(entry['data'], '%Y-%m-%d'),
                tip_tranzactie=entry['tip'],
                partener=entry['partener'],
                cui_partener='',
                valoare=entry['valoare'],
                valuta=entry['valuta'],
                tva_percent=0,
                valoare_tva=0,
                cont_debitor=entry.get('cont_debitor', ''),
                cont_creditor=entry.get('cont_creditor', ''),
                descriere=entry.get('descriere', ''),
                status_plata='',
                tip_document=entry['tip'],
                categorie_financiara=entry.get('categorie', ''),
                extra_data=entry
            )
            db.session.add(tranzactie)

        db.session.commit()
        flash("✅ Tranzacțiile bancare au fost importate cu succes.")

    except Exception as e:
        flash(f"❌ Eroare la importul datelor bancare: {e}")

    return redirect(url_for('upload_routes.upload_file'))
