from flask import Blueprint, Response
from models import db, TranzactieEFactura
from lxml import etree

transform_xml_bp = Blueprint("transform_xml_bp", __name__)


def generate_invoice_xml(invoice_number):
    invoice = db.session.query(TranzactieEFactura).filter_by(invoice_number=invoice_number).first()
    if not invoice:
        raise Exception("Factura nu există.")

    cbc = "urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2"
    root = etree.Element("Invoice", nsmap={"cbc": cbc})

    etree.SubElement(root, etree.QName(cbc, "ID")).text = invoice.invoice_number
    etree.SubElement(root, etree.QName(cbc, "IssueDate")).text = invoice.issue_date.isoformat()
    etree.SubElement(root, etree.QName(cbc, "InvoiceTypeCode")).text = invoice.invoice_type or "380"
    etree.SubElement(root, etree.QName(cbc, "DocumentCurrencyCode")).text = invoice.currency or "RON"

    supplier = etree.SubElement(root, "AccountingSupplierParty")
    etree.SubElement(supplier, etree.QName(cbc, "CompanyID")).text = invoice.supplier_cui or "RO12345678"
    etree.SubElement(supplier, etree.QName(cbc, "Name")).text = invoice.supplier_name or "Firma Emitenta"

    buyer = etree.SubElement(root, "AccountingCustomerParty")
    etree.SubElement(buyer, etree.QName(cbc, "CompanyID")).text = invoice.buyer_cui
    etree.SubElement(buyer, etree.QName(cbc, "Name")).text = invoice.buyer_name

    line = etree.SubElement(root, "InvoiceLine")
    etree.SubElement(line, etree.QName(cbc, "ID")).text = "1"
    etree.SubElement(line, etree.QName(cbc, "InvoicedQuantity")).text = str(invoice.quantity)
    etree.SubElement(line, etree.QName(cbc, "LineExtensionAmount")).text = f"{invoice.line_total:.2f}"

    item = etree.SubElement(line, "Item")
    etree.SubElement(item, etree.QName(cbc, "Description")).text = invoice.product_description

    price = etree.SubElement(line, "Price")
    etree.SubElement(price, etree.QName(cbc, "PriceAmount")).text = f"{invoice.unit_price:.2f}"

    total = etree.SubElement(root, "LegalMonetaryTotal")
    etree.SubElement(total, etree.QName(cbc, "PayableAmount")).text = f"{invoice.total_amount:.2f}"

    return etree.tostring(root, pretty_print=True, xml_declaration=True, encoding="UTF-8")


@transform_xml_bp.route("/download-xml", methods=["GET"])
def download_xml_by_invoice_number():
    from flask import request
    invoice_number = request.args.get("invoice_number")
    if not invoice_number:
        return "Parametru 'invoice_number' lipsă.", 400
    try:
        xml_bytes = generate_invoice_xml(invoice_number)
        filename = f"{invoice_number}.xml"
        return Response(
            xml_bytes,
            mimetype='application/xml',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
    except Exception as e:
        return str(e), 500
