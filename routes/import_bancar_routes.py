from flask import Blueprint, jsonify, flash, redirect, url_for
from models import db, Tranzactie
from datetime import datetime
import requests
import hashlib
import os, json

bancar_bp = Blueprint('bancar_bp', __name__)


# Funcție comună pentru încărcarea datelor bancare din fișier JSON
def load_bancar_data():
    file_path = os.path.join('uploads', 'bancar_mock_all_docker.json')
    print(f">>> Se încarcă date bancare din: {file_path}")
    with open(file_path, encoding='utf-8') as f:
        return json.load(f)


@bancar_bp.route('/import-bancar')
def import_bancar():
    try:
        data = load_bancar_data()
        added_count = 0
        for entry in data:
            id_tranzactie = entry.get("id_tranzactie")
            if not id_tranzactie or str(id_tranzactie).lower() == 'nan':
                key = f"{entry.get('data')}_{entry.get('valoare')}_{entry.get('partener')}_{entry.get('tip')}"
                id_tranzactie = hashlib.sha1(key.encode()).hexdigest()

            existing = Tranzactie.query.filter_by(id_tranzactie=id_tranzactie).first()
            if existing:
                continue

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
            added_count += 1

        db.session.commit()
        flash(f"{added_count} tranzacții bancare au fost importate cu succes.", category="bancar")

    except Exception as e:
        flash(f"Eroare la importul datelor bancare: {e}", category="bancar")

    return redirect(url_for('upload_bp.upload_file'))  # ajustează cu blueprint-ul corect
