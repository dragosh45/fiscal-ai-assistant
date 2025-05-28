# 🧾 ContabilAI – Fiscal Monitoring & VAT Automation Platform

**Deployed on Fly.io:**  
👉 [https://contabil-ai.fly.dev](https://contabil-ai.fly.dev)

ContabilAI is a lightweight ETL + AI system that helps Romanian businesses:

- Upload accounting documents (SmartBill/Custom/Bank API)
- Transform them into ANAF-compliant e-Invoices
- Calculate VAT declarations (D300/D394)
- Detect anomalies
- Export XML files ready for submission

---

## 🚀 Key Features

### 📤 Upload Accounting Documents (CSV/XLSX)
- Supports SmartBill exports or custom spreadsheets
- Automatic format detection and normalization into a unified internal schema

### 🏦 Bank API Import (mock)
- Simulates integration with banking transaction APIs
- JSON-based mock transactions imported into the database

### 📄 e-Factura Normalization & XML Generation (ANAF)
- Converts transactions to UBL RO_CIUS XML
- Downloads valid e-Invoice XML for SPV/ANAF platform

### 📊 VAT Automation & Declarations
- Detects collected and deductible VAT
- Generates D300 & D394 XML declarations

### 🧠 AI-Powered Analytics (coming soon)
- KPIs: Monthly revenue, due invoices, collected VAT
- Forecasting: Future income & cash flow
- Anomaly detection: Duplicated invoices, suspicious values

---

## 🛠️ Technologies Used

| Component | Technology | Purpose |
|----------|------------|---------|
| Backend | Flask + SQLAlchemy | Lightweight, fast, Python-native |
| Database | PostgreSQL | Relational, scalable, reliable |
| ETL | pandas | Tabular data manipulation |
| XML Export | lxml | ANAF-compliant UBL format |
| Containerization | Docker + docker-compose | Consistency and easy deploy |
| Production | gunicorn | WSGI server for Flask |
| Frontend UI | HTML + Bootstrap | Simple upload interface |

---

## 📁 Project Structure

fiscal-ai-assistant/
│
├── main.py # Flask entry point
├── config.py # DB config
├── requirements.txt # Python dependencies
├── Dockerfile # Web service Docker build
├── docker-compose.yml # PostgreSQL + Flask stack config
├── models.py # SQLAlchemy DB models
│
├── routes/ # Modular route handling
│ ├── upload_file_routes.py
│ ├── import_bancar_routes.py
│ ├── transform_efactura_routes.py
│ └── transform_efactura_to_xml_routes.py
│
├── templates/ # HTML upload form
│ └── upload.html
├── uploads/ # Uploaded/generated files
└── .env.local / .env.docker # Environment variables


---

## 🧪 Running Locally

### ▶️ With PostgreSQL Installed

1. Install dependencies:
```bash
pip install -r requirements.txt
Set up .env.local:

env
Copy
Edit
DB_USER=postgres
DB_PASSWORD=your_pass
DB_HOST=localhost
DB_PORT=5432
DB_NAME=tranzactii_DB
FLASK_ENV=development
Launch the app:

bash
Copy
Edit
python main.py
🐳 With Docker (Recommended)
Set up .env.docker:

env
Copy
Edit
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=tranzactii_db
DB_HOST=db
DB_PORT=5432
Start app:

bash
Copy
Edit
docker-compose up --build
Access UI:
http://localhost:5000

📂 Test Files (included/mocked)
mock_smartbill.csv – SmartBill invoice sample

mock_propriu.csv – Custom transaction example

bancar_mock_all.json – Bank API mock response

📌 Suggested Extensions
🧠 Integrate AI/ML: anomaly detection, clustering, predictions

☁️ CI/CD deployment: Fly.io / Render / GCP with GitHub Actions

🧾 Export invoices as PDF + e-signature (eIDAS)

