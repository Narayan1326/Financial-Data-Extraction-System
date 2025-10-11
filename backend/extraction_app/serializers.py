from rest_framework import serializers
from .models import PDFDocument, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'date', 'description', 'amount', 'category', 'transaction_type']

class PDFDocumentSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = PDFDocument
        fields = ['id', 'filename', 'uploaded_at', 'file_size', 'processed', 'transactions']