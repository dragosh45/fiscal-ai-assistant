
# 🧾 DataFlowDynamics – Fiscal Monitoring & VAT Automation Platform

A lightweight ETL + AI system that helps Romanian businesses upload accounting documents (SmartBill/Custom/Bank API), transform them into ANAF-compliant e-Invoices, calculate VAT declarations (D300/D394), detect anomalies, and export XML files ready for submission.

---

## 🔧 Key Features

👤 **Upload Accounting Documents (CSV/XLSX):**
- Supports SmartBill exports or manually structured spreadsheets.
- Automatic format detection and normalization into a unified internal schema.

🏦 **Bank API Import (mock):**
- Simulates integration with banking transaction APIs.
- JSON-based demo transactions imported into the database.

📄 **e-Factura Normalization & XML Generation (ANAF):**
- Converts normalized transactions into UBL RO_CIUS XML format.
- Downloads valid e-Invoice XML for SPV/ANAF platform.

📊 **VAT Automation & Declarations:**
- Detects VAT automatically (collected/deductible).
- Generates XML-ready Romanian D300 & D394 declarations.

📈 **AI-Powered Analytics (coming soon):**
- KPIs: monthly revenue, due invoices, collected VAT.
- Forecasting: future income & cash flow.
- Anomaly detection: duplicated invoices, suspicious values.

---

## 🛠️ Technologies Used

| Component       | Technology              | Reason |
|----------------|--------------------------|--------|
| Backend         | Flask + SQLAlchemy       | Lightweight, fast, Python-native |
| Database        | PostgreSQL               | Reliable, relational, scalable |
| ETL             | pandas                   | Efficient tabular data manipulation |
| XML Export      | `lxml`                   | ANAF-compatible structured output |
| Containerized   | Docker + docker-compose  | Easy deploy & consistency |
| Production WSGI | gunicorn                 | Scalable production Flask server |
| Frontend UI     | HTML + Bootstrap         | Simple web UI for user operations |

---

## 📁 Project Structure

```
code_for_readme/
│
├── main.py                     # Flask entry point
├── config.py                   # DB config, .env handling
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Web service Docker build
├── docker-compose.yml          # PostgreSQL + Flask app config
├── models.py                   # SQLAlchemy models
│
├── routes/                     # Modular route handling
│   ├── upload_file_routes.py
│   ├── import_bancar_routes.py
│   ├── transform_efactura_routes.py
│   └── transform_efactura_to_xml_routes.py
│
├── templates/                  # HTML upload page
│   └── upload.html
│
├── uploads/                    # Uploaded/generated files
└── .env.local / .env.docker    # Environment-specific configs
```

---

## 🚀 Installation & Running

### 🧪 Run Locally (with PostgreSQL installed):

1. Install requirements:

```bash
pip install -r requirements.txt
```

2. Set up `.env.local`:

```
DB_USER=postgres
DB_PASSWORD=your_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tranzactii_DB
FLASK_ENV=development
```

3. Launch app:

```bash
python main.py
```

---

### 🐳 Run with Docker (Recommended):

1. Set up `.env.docker`:

```
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=tranzactii_db
DB_HOST=db
DB_PORT=5432
```

2. Start app with:

```bash
docker-compose up --build
```

3. Access the UI at: `http://localhost:5000`

---

## 📁 Test Files (included or mock):

- `mock_smartbill.csv` – SmartBill invoice example
- `mock_propriu.csv` – Custom transaction file
- `bancar_mock_all.json` – Bank API mock response

---

## 📌 Suggested Extensions

- 🧠 Integrate AI/ML (anomaly detection, clustering, predictions)
- ☁️ CI/CD deploy to Fly.io / Render / GCP using GitHub Actions
- 📄 Export e-Invoices as PDF + electronic signature (eIDAS)

