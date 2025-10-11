import re
from typing import List, Dict, Any

class CategoryClassifier:
    def __init__(self):
        # Enhanced category patterns for better classification
        self.category_patterns = {
            'food': [
                r'.*GROCERY.*', r'.*FOOD.*', r'.*RESTAURANT.*', r'.*CAFE.*', 
                r'.*COFFEE.*', r'.*BAKERY.*', r'.*SUPERMARKET.*', r'.*EATERY.*',
                r'.*BURGER.*', r'.*PIZZA.*', r'.*HOTEL.*'
            ],
            'shopping': [
                r'.*AMAZON.*', r'.*WALMART.*', r'.*TARGET.*', r'.*MALL.*',
                r'.*SHOPPING.*', r'.*RETAIL.*', r'.*STORE.*', r'.*PURCHASE.*',
                r'.*MARKET.*'
            ],
            'transport': [
                r'.*GAS.*', r'.*SHELL.*', r'.*EXXON.*', r'.*UBER.*',
                r'.*LYFT.*', r'.*TAXI.*', r'.*TRANSPORT.*', r'.*AUTO.*',
                r'.*PETROL.*', r'.*FUEL.*'
            ],
            'entertainment': [
                r'.*MOVIE.*', r'.*CINEMA.*', r'.*NETFLIX.*', r'.*SPOTIFY.*',
                r'.*ENTERTAINMENT.*', r'.*GAME.*', r'.*THEATER.*'
            ],
            'bills': [
                r'.*ELECTRIC.*', r'.*WATER.*', r'.*GAS.*BILL.*', r'.*UTILITY.*',
                r'.*PHONE.*', r'.*INTERNET.*', r'.*CABLE.*', r'.*BILL.*PAYMENT.*',
                r'.*BSNL.*', r'.*VODAFONE.*', r'.*MSEDCL.*'
            ],
            'income': [
                r'.*SALARY.*', r'.*DEPOSIT.*', r'.*PAYCHECK.*', r'.*INCOME.*',
                r'.*TRANSFER.*FROM.*', r'.*REFUND.*', r'.*INTEREST.*',
                r'.*NEFT.*CR.*', r'.*RTGS.*CR.*', r'.*IMPS.*CR.*'
            ],
            'transfer': [
                r'.*TRANSFER.*', r'.*ZELLE.*', r'.*VENMO.*', r'.*PAYPAL.*',
                r'.*UPI.*', r'.*NEFT.*', r'.*RTGS.*', r'.*IMPS.*'
            ],
            'healthcare': [
                r'.*HOSPITAL.*', r'.*MEDICAL.*', r'.*DOCTOR.*', r'.*PHARMACY.*',
                r'.*HEALTH.*', r'.*CLINIC.*'
            ],
            'business': [
                r'.*GAS.*AGENCY.*', r'.*BUSINESS.*', r'.*OFFICE.*', r'.*SUPPLY.*',
                r'.*WHOLESALE.*', r'.*DISTRIBUTOR.*'
            ]
        }
    
    def classify_transactions(self, transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Classify transactions into categories based on description patterns
        """
        classified_transactions = []
        
        for transaction in transactions:
            description = transaction['description'].upper()
            category = 'other'
            confidence = 0.0
            
            # Check each category pattern
            for cat, patterns in self.category_patterns.items():
                for pattern in patterns:
                    if re.match(pattern, description, re.IGNORECASE):
                        category = cat
                        confidence = 0.9
                        break
                if category != 'other':
                    break
            
            # Special rules based on transaction type and amount
            if category == 'other':
                category = self._apply_special_rules(transaction, description)
                confidence = 0.7
            
            # Special rule for income based on amount and type
            if transaction['amount'] > 0 and transaction['type'] == 'credit':
                if any(word in description for word in ['SALARY', 'DEPOSIT', 'PAYCHECK', 'INTEREST']):
                    category = 'income'
                    confidence = 0.95
                elif category == 'other':
                    category = 'income'
                    confidence = 0.8
            
            classified_transactions.append({
                **transaction,
                'category': category,
                'confidence_score': confidence
            })
        
        return classified_transactions
    
    def _apply_special_rules(self, transaction: Dict[str, Any], description: str) -> str:
        """
        Apply special classification rules based on transaction characteristics
        """
        amount = abs(transaction['amount'])
        
        # Gas agency business transactions
        if 'GAS' in description and 'AGENCY' in description:
            return 'business'
        
        # Hospital/medical transactions
        if any(word in description for word in ['HOSPITAL', 'MEDICAL', 'CLINIC', 'PHARMACY']):
            return 'healthcare'
        
        # Large transfers
        if amount > 10000 and any(word in description for word in ['TRANSFER', 'NEFT', 'RTGS']):
            return 'transfer'
        
        # Small recurring payments
        if amount < 1000 and any(word in description for word in ['BILL', 'RECHARGE', 'PAYMENT']):
            return 'bills'
        
        return 'other'