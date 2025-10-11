import PyPDF2
import pdfplumber
import re
from typing import List, Dict, Any

class PDFExtractor:
    def __init__(self):
        self.supported_banks = [
            'hdfc', 'bank of america', 'wells fargo', 'citi', 'capital one',
            'indian bank', 'punjab national bank', 'state bank of india', 'icici'
        ]
    
    def extract_text(self, pdf_path: str) -> str:
        """
        Extract text from PDF using multiple methods for better accuracy
        """
        text = ""
        
        # Method 1: Try pdfplumber first (better for table extraction)
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    # Try to extract tables first
                    tables = page.extract_tables()
                    if tables:
                        for table in tables:
                            for row in table:
                                if row:
                                    text += ' | '.join([str(cell) if cell else '' for cell in row]) + "\n"
                    
                    # Then extract text
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"pdfplumber extraction failed: {e}")
        
        # Method 2: Fall back to PyPDF2
        if not text.strip():
            try:
                with open(pdf_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
            except Exception as e:
                print(f"PyPDF2 extraction failed: {e}")
        
        return text
    
    def detect_bank(self, text: str) -> str:
        """
        Detect the bank from the extracted text with improved pattern matching
        """
        text_lower = text.lower()
        
        bank_patterns = {
            'hdfc': [r'hdfc\s+bank', r'we understand your world'],
            'indian bank': [r'indian\s+bank', r'idib\d+', r'statement of account'],
            'pnb': [r'punjab national bank', r'pnb'],
            'sbi': [r'state bank of india', r'sbi'],
            'icici': [r'icici\s+bank'],
            'axis': [r'axis\s+bank'],
            'kotak': [r'kotak\s+mahindra']
        }
        
        for bank, patterns in bank_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return bank
        
        return "unknown"
    
    def detect_account_type(self, text: str) -> str:
        """
        Detect account type from statement text
        """
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['current account', 'ca-', 'current']):
            return 'current'
        elif any(word in text_lower for word in ['savings', 'sb-', 'savings account']):
            return 'savings'
        elif any(word in text_lower for word in ['od', 'overdraft']):
            return 'overdraft'
        else:
            return 'unknown'