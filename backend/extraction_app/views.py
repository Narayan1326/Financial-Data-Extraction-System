from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
import os
import json
from datetime import datetime
from typing import List, Dict

from .models import PDFDocument, Transaction
from .serializers import TransactionSerializer
from .ml_services.pdf_extractor import PDFExtractor
from .ml_services.transaction_parser import TransactionParser
from .ml_services.category_classifier import CategoryClassifier

@api_view(['POST'])
def upload_pdf(request):
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    file = request.FILES['file']
    if not file.name.lower().endswith('.pdf'):
        return Response({'error': 'File must be a PDF'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Save the file temporarily
    fs = FileSystemStorage()
    filename = fs.save(file.name, file)
    file_path = fs.path(filename)
    
    try:
        # Extract text from PDF
        extractor = PDFExtractor()
        extracted_text = extractor.extract_text(file_path)
        
        # Detect bank type
        bank_type = extractor.detect_bank(extracted_text)
        account_type = extractor.detect_account_type(extracted_text)
        
        # Parse transactions based on bank type
        parser = TransactionParser()
        raw_transactions = parser.parse_transactions(extracted_text, bank_type)
        
        # Classify categories
        classifier = CategoryClassifier()
        classified_transactions = classifier.classify_transactions(raw_transactions)
        
        # Create PDF document record
        document = PDFDocument.objects.create(
            filename=file.name,
            file_size=file.size,
            processed=True,
            bank_type=bank_type,
            account_type=account_type
        )
        
        # Create transaction records
        transactions_created = 0
        for transaction_data in classified_transactions:
            try:
                Transaction.objects.create(
                    document=document,
                    date=datetime.strptime(transaction_data['date'], '%Y-%m-%d').date(),
                    description=transaction_data['description'],
                    amount=transaction_data['amount'],
                    category=transaction_data['category'],
                    transaction_type=transaction_data['type'],
                    confidence_score=transaction_data.get('confidence_score', 0.5)
                )
                transactions_created += 1
            except Exception as e:
                print(f"Error creating transaction: {e}")
                continue
        
        # Generate summary statistics
        summary = _generate_transaction_summary(classified_transactions)
        
        # Clean up temporary file
        if os.path.exists(file_path):
            os.remove(file_path)
        
        return Response({
            'message': f'Successfully processed PDF and extracted {transactions_created} transactions',
            'filename': file.name,
            'bank_type': bank_type,
            'account_type': account_type,
            'transactions_extracted': transactions_created,
            'summary': summary,
            'sample_transactions': classified_transactions[:10]  # Return first 10 as sample
        })
        
    except Exception as e:
        # Clean up temporary file in case of error
        if os.path.exists(file_path):
            os.remove(file_path)
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def _generate_transaction_summary(transactions: List[Dict]) -> Dict:
    """Generate summary statistics for transactions"""
    total_credits = sum(t['amount'] for t in transactions if t['amount'] > 0)
    total_debits = abs(sum(t['amount'] for t in transactions if t['amount'] < 0))
    
    category_totals = {}
    for transaction in transactions:
        category = transaction['category']
        amount = transaction['amount']
        if category not in category_totals:
            category_totals[category] = {'credits': 0, 'debits': 0}
        
        if amount > 0:
            category_totals[category]['credits'] += amount
        else:
            category_totals[category]['debits'] += abs(amount)
    
    return {
        'total_transactions': len(transactions),
        'total_credits': total_credits,
        'total_debits': total_debits,
        'net_balance': total_credits - total_debits,
        'category_breakdown': category_totals
    }

@api_view(['POST'])
def search_transactions(request):
    try:
        transactions = Transaction.objects.all()
        
        # Filter by date range
        date_from = request.data.get('date_from')
        date_to = request.data.get('date_to')
        
        if date_from:
            transactions = transactions.filter(date__gte=date_from)
        if date_to:
            transactions = transactions.filter(date__lte=date_to)
        
        # Filter by category
        category = request.data.get('category')
        if category:
            transactions = transactions.filter(category=category)
        
        # Filter by amount range
        min_amount = request.data.get('min_amount')
        max_amount = request.data.get('max_amount')
        
        if min_amount:
            transactions = transactions.filter(amount__gte=min_amount)
        if max_amount:
            transactions = transactions.filter(amount__lte=max_amount)
        
        # Filter by transaction type
        transaction_type = request.data.get('transaction_type')
        if transaction_type:
            if transaction_type == 'credit':
                transactions = transactions.filter(amount__gt=0)
            elif transaction_type == 'debit':
                transactions = transactions.filter(amount__lt=0)
        
        # Filter by bank type
        bank_type = request.data.get('bank_type')
        if bank_type:
            transactions = transactions.filter(document__bank_type=bank_type)
        
        serializer = TransactionSerializer(transactions, many=True)
        return Response({
            'transactions': serializer.data,
            'count': len(serializer.data)
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
def transaction_categories(request):
    categories = dict(Transaction.CATEGORY_CHOICES)
    return Response({'categories': categories})

@api_view(['GET'])
def bank_types(request):
    """Get unique bank types from processed documents"""
    bank_types = PDFDocument.objects.values_list('bank_type', flat=True).distinct()
    return Response({'bank_types': list(bank_types)})