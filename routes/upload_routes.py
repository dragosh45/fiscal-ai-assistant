from flask import Blueprint, render_template, request, redirect, flash, current_app
from models import db, Tranzactie
import pandas as pd
import os
import json
import hashlib  # sub celelalte importuri

upload_blueprint = Blueprint("upload_routes", __name__)


def detect_and_transform(df):
    if "Număr document" in df.columns:
        sursa = "SmartBill"
        df_trans = pd.DataFrame()
        df_trans["id_tranzactie"] = None
        df_trans["sursa"] = sursa
        df_trans["data_tranzactie"] = pd.to_datetime(
            df["Data emiterii"], errors="coerce"
        )
        df_trans["tip_tranzactie"] = df["Tip document"]
        df_trans["partener"] = df["Nume client"]
        df_trans["cui_partener"] = df.get("CIF client", "")
        df_trans["valoare"] = pd.to_numeric(df["Valoare totală"], errors="coerce")
        df_trans["valoare_tva"] = pd.to_numeric(df["Valoare TVA"], errors="coerce")
        df_trans["valuta"] = df.get("Valută", "RON")
        df_trans["status_plata"] = df.get("Status plată", "")
        df_trans["descriere"] = df.get("Descriere", "")
        df_trans["tip_document"] = df["Tip document"]
        df_trans["categorie_financiara"] = ""
        df_trans["cont_debitor"] = ""
        df_trans["cont_creditor"] = ""
        return df_trans, sursa

    elif "Data tranzacție" in df.columns:
        sursa = "Propriu"
        df_trans = pd.DataFrame()
        df_trans["id_tranzactie"] = None
        df_trans["sursa"] = sursa
        df_trans["data_tranzactie"] = pd.to_datetime(
            df["Data tranzacție"], errors="coerce"
        )
        df_trans["tip_tranzactie"] = df["Tip tranzacție"]
        df_trans["partener"] = df["Client/Furnizor"]
        df_trans["cui_partener"] = ""
        df_trans["valoare"] = pd.to_numeric(df["Valoare"], errors="coerce")
        df_trans["tva_percent"] = pd.to_numeric(df["TVA (%)"], errors="coerce")
        df_trans["valoare_tva"] = (
                df_trans["valoare"] * (df_trans["tva_percent"] / 100)
        ).round(2)
        df_trans["valuta"] = "RON"
        df_trans["status_plata"] = ""
        df_trans["descriere"] = df.get("Detalii", "")
        df_trans["tip_document"] = df["Tip tranzacție"]
        df_trans["categorie_financiara"] = df["Categorie"]
        df_trans["cont_debitor"] = ""
        df_trans["cont_creditor"] = ""
        return df_trans, sursa

    else:
        raise ValueError("⚠️ Nu am putut detecta formatul fișierului!")


def generate_id_tranzactie(row):
    key = f"{row['data_tranzactie']}_{row['valoare']}_{row['partener']}_{row['tip_tranzactie']}"
    return hashlib.sha1(key.encode()).hexdigest()


@upload_blueprint.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")

        if not file:
            flash("⚠️ Selectează un fișier CSV sau XLSX.")
            return redirect("/")

        filename = file.filename
        path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        file.save(path)

        try:
            df = pd.read_csv(path) if filename.endswith(".csv") else pd.read_excel(path)
            df_trans, sursa = detect_and_transform(df)

            for _, row in df_trans.iterrows():
                # Preluăm id_tranzactie
                id_tranzactie = row.get('id_tranzactie')

                # Dacă este lipsit sau NaN, îl generăm
                if not id_tranzactie or str(id_tranzactie).lower() == 'nan':
                    id_tranzactie = generate_id_tranzactie(row)
                    row['id_tranzactie'] = id_tranzactie

                # Căutăm în baza de date după id_tranzactie (ca string)
                existing = Tranzactie.query.filter_by(id_tranzactie=str(id_tranzactie)).first()
                if existing:
                    continue  # Sărim peste duplicate

                # Inserăm tranzacția nouă
                tranzactie = Tranzactie(
                    id_tranzactie=row.get("id_tranzactie"),
                    sursa=sursa,
                    data_tranzactie=row.get("data_tranzactie"),
                    tip_tranzactie=row.get("tip_tranzactie"),
                    partener=row.get("partener"),
                    cui_partener=row.get("cui_partener"),
                    valoare=row.get("valoare"),
                    valuta=row.get("valuta"),
                    tva_percent=row.get("tva_percent"),
                    valoare_tva=row.get("valoare_tva"),
                    cont_debitor=row.get("cont_debitor"),
                    cont_creditor=row.get("cont_creditor"),
                    descriere=row.get("descriere"),
                    status_plata=row.get("status_plata"),
                    tip_document=row.get("tip_document"),
                    categorie_financiara=row.get("categorie_financiara"),
                    extra_data=json.loads(row.to_json()),
                )
                db.session.add(tranzactie)
            db.session.commit()

            flash(
                f"✅ Fișier '{filename}' procesat și salvat cu succes ca sursă: {sursa}."
            )

        except Exception as e:
            flash(f"❌ Eroare la procesare: {e}")
        return redirect("/")

    return render_template("upload.html")
