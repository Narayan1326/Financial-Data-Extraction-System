# AI-Powered Financial Data Extraction System

A comprehensive system for extracting structured financial data from PDF bank statements using AI/ML techniques.

## Architecture

- **Frontend**: Flask web application for user interface
- **Backend**: Django REST API for data processing
- **Database**: SQLite (default) or PostgreSQL
- **ML/NLP**: Custom models for transaction parsing and categorization

## Features

- 📤 PDF bank statement upload
- 🤖 AI-powered transaction extraction
- 🏷️ Automatic category classification
- 🔍 Advanced querying and filtering
- 📊 Monthly summaries and analytics
- 🔒 User data isolation

## Quick Start

### Prerequisites

- Python 3.8+
- pip (Python package manager)

### Installation

#### Quick Start (Recommended)
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Finance
   ```

2. **Start all services automatically**
   
   **For Windows:**
   ```bash
   start_all.bat
   ```
   
   **For Windows (PowerShell):**
   ```bash
   .\start_all.bat
   ```

#### Manual Setup

1. **Setup Backend (Django)**
   ```bash
   cd backend
   # Create virtual environment (if not exists)
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Run migrations
   python manage.py migrate
   
   # Start server
   python manage.py runserver 0.0.0.0:8000
   ```
   
   Backend will run on http://localhost:8000

2. **Setup Frontend (Flask)**
   ```bash
   cd ../frontend
   # Create virtual environment (if not exists)
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # Linux/Mac:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start server
   python app.py
   ```
   
   Frontend will run on http://localhost:5000

#### Using Docker (Alternative)
```bash
docker-compose up --build
```

### Usage ###

1.Access the application at http://localhost:5000
2.Upload a PDF bank statement using the upload interface
3.Query transactions using the query interface
4.View analytics and monthly summaries

**API Endpoints**

### Transactions
1. GET /api/transactions/ - List all transactions
2. POST /api/transactions/upload_pdf/ - Upload and extract PDF
3. GET /api/transactions/monthly_summary/ - Get monthly summary
4. GET /api/transactions/by_category/ - Filter by category

### Query Parameters
1. month - Filter by month (1-12)
2. year - Filter by year
3. category - Filter by category
4. type - Filter by transaction type

**Project Structure**

Finance/
├── frontend/                 # Flask application
├── backend/                  # Django application
├── data/                     # Sample PDFs
├── docker-compose.yml        # Docker configuration
├── start_*.bat              # Windows startup scripts
└── README.md

**ML Components**
PDF Extraction
Uses pdfplumber and PyPDF2 for robust text extraction

Multiple regex patterns for different bank formats

Layout analysis for complex statements

Category Classification
Random Forest classifier with TF-IDF features

Rule-based fallback system

Trainable with new data

Database Models
Transaction
id (Primary Key)

user (ForeignKey)

date (Date)

description (Text)

amount (Decimal)

type (Choice: Credit/Debit)

category (Choice: Food, Shopping, etc.)

balance (Decimal)

Development
Adding New Bank Formats
Update regex patterns in pdf_extractor.py

Add new date formats in transaction parser

Test with sample statements

Training Category Model
Add training data in category_classifier.py

Run retraining method

Validate with test transactions

**Deployment**

### Using Docker (Optional)
    ```bash
    docker-compose up --build