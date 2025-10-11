from django.contrib import admin
from .models import PDFDocument, Transaction

@admin.register(PDFDocument)
class PDFDocumentAdmin(admin.ModelAdmin):
    list_display = ['filename', 'uploaded_at', 'file_size', 'processed']
    list_filter = ['processed', 'uploaded_at']
    search_fields = ['filename']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'description', 'amount', 'category', 'transaction_type', 'document']
    list_filter = ['category', 'transaction_type', 'date']
    search_fields = ['description']
    date_hierarchy = 'date'