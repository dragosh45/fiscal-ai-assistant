from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

db = SQLAlchemy()


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


class TranzactieEFactura(db.Model):
    __tablename__ = 'tabel_tranzactii_efactura'

    id = db.Column(db.Integer, primary_key=True)
    invoice_number = db.Column(db.String(100))
    issue_date = db.Column(db.Date)
    currency = db.Column(db.String(3))
    supplier_name = db.Column(db.String(255))
    supplier_cui = db.Column(db.String(50))
    buyer_name = db.Column(db.String(255))
    buyer_cui = db.Column(db.String(50))
    product_code = db.Column(db.String(100))
    product_description = db.Column(db.Text)
    quantity = db.Column(db.Float)
    unit_price = db.Column(db.Float)
    vat_rate = db.Column(db.Float)
    vat_amount = db.Column(db.Float)
    line_total = db.Column(db.Float)
    total_amount = db.Column(db.Float)
    payment_due_date = db.Column(db.Date)
    invoice_type = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
