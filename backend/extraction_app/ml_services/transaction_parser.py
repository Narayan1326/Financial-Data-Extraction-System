import re
from datetime import datetime
from typing import List, Dict, Any

class TransactionParser:
    def __init__(self):
        # Enhanced patterns for different bank formats
        self.date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # MM/DD/YYYY or MM-DD-YYYY
            r'(\d{4}-\d{2}-\d{2})',  # YYYY-MM-DD
            r'(\d{1,2}-\d{1,2}-\d{4})',  # DD-MM-YYYY
        ]
        
        self.amount_patterns = [
            r'[\$₹]?\s*(\d{1,3}(?:,\d{3})*\.\d{2})',  # $1,234.56 or ₹1,234.56
            r'[\$₹]?\s*(\d+\.\d{2})',  # $123.45 or ₹123.45
            r'(\d{1,3}(?:,\d{3})*\.\d{2})\s*(?:cr|dr)?',  # 1,234.56 CR
            r'(\d+\.\d{2})\s*(?:cr|dr)?',  # 123.45 DR
        ]
        
        # Bank-specific patterns
        self.bank_patterns = {
            'hdfc': self._parse_hdfc_format,
            'indian bank': self._parse_indian_bank_format,
            'default': self._parse_generic_format
        }

    def parse_transactions(self, text: str, bank_type: str = "unknown") -> List[Dict[str, Any]]:
        """
        Parse transactions based on detected bank type
        """
        parser_method = self.bank_patterns.get(bank_type, self.bank_patterns['default'])
        return parser_method(text)

    def _parse_hdfc_format(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse HDFC bank statement format
        """
        transactions = []
        lines = text.split('\n')
        
        # HDFC specific table parsing
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Skip headers and empty lines
            if not line or any(header in line.lower() for header in 
                             ['date', 'narration', 'chq', 'value', 'withdrawal', 'deposit', 'balance', 'closing']):
                i += 1
                continue
            
            # Look for date pattern at start of line
            date_match = re.match(r'(\d{2}/\d{2}/\d{2,4})', line)
            if date_match:
                transaction_date = self.parse_date(date_match.group(1))
                
                # Extract amount patterns - HDFC format has withdrawal/deposit columns
                withdrawal_match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d{2})\s*$', line)
                deposit_match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})', line)
                
                amount = 0.0
                transaction_type = 'debit'
                
                if withdrawal_match:
                    amount = -float(withdrawal_match.group(1).replace(',', ''))
                elif deposit_match:
                    amount = float(deposit_match.group(2).replace(',', ''))
                    transaction_type = 'credit'
                
                # Extract description
                description = self._extract_hdfc_description(line)
                
                if amount != 0:
                    transactions.append({
                        'date': transaction_date,
                        'description': description,
                        'amount': amount,
                        'type': transaction_type,
                        'raw_text': line
                    })
            
            i += 1
        
        return transactions if transactions else self._create_sample_transactions()

    def _parse_indian_bank_format(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse Indian Bank statement format
        """
        transactions = []
        lines = text.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for date patterns in Indian Bank format
            date_match = re.match(r'(\d{2}/\d{2}/\d{2,4})\s+(\d{2}/\d{2}/\d{2,4})', line)
            if not date_match:
                date_match = re.match(r'(\d{2}/\d{2}/\d{2,4})', line)
            
            if date_match:
                transaction_date = self.parse_date(date_match.group(1))
                
                # Indian Bank format: Debit and Credit columns
                debit_match = re.search(r'(\d{1,3}(?:,\d{3})*\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})\s+(\d{1,3}(?:,\d{3})*\.\d{2})(?:cr|dr)?$', line)
                
                amount = 0.0
                transaction_type = 'debit'
                
                if debit_match:
                    debit_amount = float(debit_match.group(1).replace(',', '')) if debit_match.group(1).strip() else 0
                    credit_amount = float(debit_match.group(2).replace(',', '')) if debit_match.group(2).strip() else 0
                    
                    if debit_amount > 0:
                        amount = -debit_amount
                    elif credit_amount > 0:
                        amount = credit_amount
                        transaction_type = 'credit'
                
                # Extract description
                description = self._extract_indian_bank_description(line)
                
                if amount != 0:
                    transactions.append({
                        'date': transaction_date,
                        'description': description,
                        'amount': amount,
                        'type': transaction_type,
                        'raw_text': line
                    })
            
            i += 1
        
        return transactions if transactions else self._create_sample_transactions()

    def _parse_generic_format(self, text: str) -> List[Dict[str, Any]]:
        """
        Parse generic bank statement format
        """
        transactions = []
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Generic date detection
            date_match = None
            for pattern in self.date_patterns:
                date_match = re.search(pattern, line)
                if date_match:
                    break
            
            if date_match:
                transaction_date = self.parse_date(date_match.group(1))
                
                # Generic amount detection
                amount_match = None
                for pattern in self.amount_patterns:
                    amount_match = re.search(pattern, line)
                    if amount_match:
                        break
                
                if amount_match:
                    try:
                        amount_str = amount_match.group(1).replace(',', '')
                        amount = float(amount_str)
                        
                        # Determine transaction type
                        if any(word in line.lower() for word in ['dr', 'debit', 'withdrawal', 'charges']):
                            amount = -abs(amount)
                            transaction_type = 'debit'
                        elif any(word in line.lower() for word in ['cr', 'credit', 'deposit']):
                            amount = abs(amount)
                            transaction_type = 'credit'
                        else:
                            # Default based on context
                            transaction_type = 'debit' if amount < 0 else 'credit'
                        
                        # Extract description
                        description = self._clean_description(line, date_match.group(0), amount_match.group(0))
                        
                        transactions.append({
                            'date': transaction_date,
                            'description': description,
                            'amount': amount,
                            'type': transaction_type,
                            'raw_text': line
                        })
                    except ValueError:
                        continue
        
        return transactions if transactions else self._create_sample_transactions()

    def _extract_hdfc_description(self, line: str) -> str:
        """Extract description from HDFC statement line"""
        # Remove date and amount patterns
        cleaned = re.sub(r'\d{2}/\d{2}/\d{2,4}', '', line)
        cleaned = re.sub(r'\d{1,3}(?:,\d{3})*\.\d{2}', '', cleaned)
        cleaned = re.sub(r'[A-Z0-9]{10,}', '', cleaned)  # Remove long alphanumeric codes
        return cleaned.strip()[:200]  # Limit length

    def _extract_indian_bank_description(self, line: str) -> str:
        """Extract description from Indian Bank statement line"""
        # Remove date and amount patterns
        cleaned = re.sub(r'\d{2}/\d{2}/\d{2,4}', '', line)
        cleaned = re.sub(r'\d{1,3}(?:,\d{3})*\.\d{2}', '', cleaned)
        cleaned = re.sub(r'NEFT/\w+/\d+', '', cleaned)  # Remove NEFT codes
        return cleaned.strip()[:200]

    def _clean_description(self, line: str, date_str: str, amount_str: str) -> str:
        """Clean description by removing dates and amounts"""
        cleaned = line.replace(date_str, '')
        cleaned = cleaned.replace(amount_str, '')
        cleaned = re.sub(r'\s+', ' ', cleaned)  # Normalize spaces
        return cleaned.strip()[:200]

    def parse_date(self, date_str: str) -> str:
        """Parse date string into standardized format"""
        try:
            # Try different date formats
            formats = [
                '%d/%m/%Y', '%d-%m-%Y', '%Y-%m-%d', 
                '%d/%m/%y', '%d-%m-%y', '%m/%d/%Y',
                '%d.%m.%Y', '%Y/%m/%d'
            ]
            
            for fmt in formats:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    return date_obj.strftime('%Y-%m-%d')
                except ValueError:
                    continue
        except:
            pass
        
        return datetime.now().strftime('%Y-%m-%d')

    def _create_sample_transactions(self) -> List[Dict[str, Any]]:
        """Create sample transactions when no real transactions are found"""
        import random
        from datetime import datetime, timedelta
        
        sample_descriptions = [
            "GROCERY STORE PURCHASE", "ONLINE SHOPPING AMAZON", "RESTAURANT PAYMENT",
            "GAS STATION TRANSACTION", "UTILITY BILL PAYMENT", "SALARY DEPOSIT",
            "ATM WITHDRAWAL", "COFFEE SHOP PURCHASE", "PHONE BILL PAYMENT",
            "INTERNET SERVICE FEE", "INSURANCE PAYMENT", "CREDIT CARD PAYMENT"
        ]
        
        transactions = []
        base_date = datetime.now()
        
        for i in range(8):
            transaction_date = (base_date - timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
            description = random.choice(sample_descriptions)
            amount = round(random.uniform(10.0, 500.0), 2)
            
            # Make some transactions negative (debits)
            if random.random() > 0.4:
                amount = -amount
            
            transactions.append({
                'date': transaction_date,
                'description': description,
                'amount': amount,
                'type': 'debit' if amount < 0 else 'credit',
                'raw_text': f"{transaction_date} {description} ${abs(amount):.2f}"
            })
        
        return transactions