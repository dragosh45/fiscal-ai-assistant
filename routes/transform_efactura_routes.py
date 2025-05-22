from flask import Blueprint, flash, redirect, url_for
from models import db, Tranzactie, TranzactieEFactura

transform_bp = Blueprint('transform_bp', __name__)


@transform_bp.route('/normalize-tranzactii', methods=['POST'])
def normalize_tranzactii():
    tranzactii = Tranzactie.query.all()
    counter = 0
    for t in tranzactii:
        # Verificăm dacă există deja o intrare cu același id_tranzactie
        existing = TranzactieEFactura.query.filter_by(invoice_number=t.id_tranzactie).first()
        if existing:
            continue  # Dacă există deja, trecem peste
        norm = TranzactieEFactura(
            invoice_number=t.id_tranzactie,
            issue_date=t.data_tranzactie,
            currency=t.valuta,
            supplier_name="Firma Mea SRL",  # hardcoded sau din config
            supplier_cui="12345678",
            buyer_name=t.partener,
            buyer_cui=t.cui_partener,
            product_code="GENERIC",
            product_description=t.descriere or "Serviciu/Produs",
            quantity=1,
            unit_price=t.valoare,
            vat_rate=t.tva_percent,
            vat_amount=t.valoare_tva,
            line_total=t.valoare,
            total_amount=t.valoare + (t.valoare_tva or 0),
            payment_due_date=t.data_tranzactie,  # dummy
            invoice_type="380"
        )
        db.session.add(norm)
        counter += 1
    db.session.commit()
    flash(f"{counter} tranzacții au fost normalizate.", category="efactura")
    return redirect(url_for("upload_bp.upload_file"))
