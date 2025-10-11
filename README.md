# AI-Powered Financial Data Extraction System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2.7-green.svg)](https://djangoproject.com)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-red.svg)](https://flask.palletsprojects.com)

A comprehensive system for extracting structured financial data from PDF bank statements using AI/ML techniques. This application automatically parses bank statements, categorizes transactions, and provides powerful querying capabilities.

## 🚀 Features

- 📤 **PDF Upload**: Upload bank statements in PDF format
- 🤖 **AI-Powered Extraction**: Automatic transaction parsing using ML algorithms
- 🏷️ **Smart Categorization**: Automatic category classification (Food, Shopping, Transport, etc.)
- 🔍 **Advanced Querying**: Filter transactions by date, category, amount, and more
- 📊 **Analytics Dashboard**: Monthly summaries and spending insights
- 🏦 **Multi-Bank Support**: Supports HDFC, Indian Bank, and generic bank formats
- 🔒 **Secure Processing**: Local data processing with no external API calls

## 🏗️ Architecture

- **Frontend**: Flask web application with modern UI
- **Backend**: Django REST API for data processing
- **Database**: SQLite (default) with PostgreSQL support
- **ML/NLP**: Custom models for transaction parsing and categorization
- **PDF Processing**: pdfplumber and PyPDF2 for robust text extraction

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## 🛠️ Installation

### Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-financial-extractor.git
   cd ai-financial-extractor
   ```

2. **Setup Backend (Django)**
   ```bash
   cd backend
   
   # Create virtual environment
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
   
   # Start backend server
   python manage.py runserver
   ```

3. **Setup Frontend (Flask)**
   ```bash
   cd ../frontend
   
   # Use the same virtual environment or create new one
   # If using same venv, just activate it
   # If creating new one:
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Start frontend server
   python app.py
   ```

4. **Access the Application**
   - Frontend: http://localhost:5000
   - Backend API: http://localhost:8000

### Using Docker (Alternative)

```bash
docker-compose up --build
```

## 🎯 Usage

### Web Interface

1. **Upload PDF**: Navigate to http://localhost:5000/upload and upload your bank statement
2. **View Results**: Processed transactions will be displayed with categories
3. **Search & Filter**: Use the query interface to filter transactions
4. **Analytics**: View monthly summaries and spending patterns

### API Endpoints

#### Transaction Management
- `GET /api/categories/` - Get available transaction categories
- `POST /api/upload-pdf/` - Upload and process PDF bank statement
- `POST /api/search-transactions/` - Search transactions with filters

#### Query Parameters
- `date_from` - Filter transactions from date (YYYY-MM-DD)
- `date_to` - Filter transactions to date (YYYY-MM-DD)
- `category` - Filter by category (food, shopping, transport, etc.)
- `min_amount` - Minimum transaction amount
- `max_amount` - Maximum transaction amount
- `transaction_type` - Filter by type (credit/debit)

## 📁 Project Structure

```
ai-financial-extractor/
├── backend/                    # Django REST API
│   ├── extraction_app/         # Main Django app
│   │   ├── ml_services/        # ML processing modules
│   │   │   ├── pdf_extractor.py
│   │   │   ├── transaction_parser.py
│   │   │   └── category_classifier.py
│   │   ├── models.py           # Database models
│   │   ├── views.py            # API views
│   │   └── serializers.py      # Data serializers
│   ├── financial_extraction/   # Django project settings
│   ├── requirements.txt        # Backend dependencies
│   └── manage.py              # Django management script
├── frontend/                   # Flask web application
│   ├── templates/              # HTML templates
│   ├── static/                 # CSS and JavaScript
│   ├── app.py                 # Flask application
│   └── requirements.txt       # Frontend dependencies
├── data/                       # Sample data and PDFs
│   ├── sample_pdfs/           # Sample bank statements
│   └── extracted/             # Processed data
├── docker-compose.yml         # Docker configuration
└── README.md                  # This file
```

## 🤖 ML Components

### PDF Extraction
- **pdfplumber**: Primary PDF text extraction with table support
- **PyPDF2**: Fallback extraction method
- **Multi-format Support**: Handles various bank statement layouts
- **Robust Parsing**: Handles scanned PDFs and complex layouts

### Transaction Parsing
- **Bank-Specific Patterns**: Custom regex patterns for different banks
- **Date Recognition**: Multiple date format support
- **Amount Extraction**: Handles various currency formats
- **Description Cleaning**: Removes noise and extracts meaningful descriptions

### Category Classification
- **Rule-Based System**: Pattern matching for common transaction types
- **Confidence Scoring**: Provides confidence levels for classifications
- **Extensible**: Easy to add new categories and patterns
- **Fallback Logic**: Handles edge cases gracefully

## 🗄️ Database Models

### PDFDocument
- `filename`: Original PDF filename
- `file_size`: File size in bytes
- `processed`: Processing status
- `bank_type`: Detected bank type
- `account_type`: Account type (savings/current)

### Transaction
- `date`: Transaction date
- `description`: Transaction description
- `amount`: Transaction amount (positive for credit, negative for debit)
- `category`: Transaction category (food, shopping, transport, etc.)
- `transaction_type`: Credit or debit
- `confidence_score`: ML confidence score

## 🙏 Acknowledgments

- Django and Django REST Framework
- Flask web framework
- pdfplumber and PyPDF2 for PDF processing
- Bootstrap for UI components

---

**Made with ❤️ for financial data automation**
