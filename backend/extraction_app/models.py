from django.db import models

class PDFDocument(models.Model):
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.IntegerField()
    processed = models.BooleanField(default=False)
    bank_type = models.CharField(max_length=50, default='unknown')
    account_type = models.CharField(max_length=20, default='unknown')
    
    def __str__(self):
        return f"{self.filename} ({self.bank_type})"

class Transaction(models.Model):
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('shopping', 'Shopping'),
        ('transport', 'Transportation'),
        ('entertainment', 'Entertainment'),
        ('bills', 'Bills & Utilities'),
        ('income', 'Income'),
        ('transfer', 'Transfers'),
        ('healthcare', 'Healthcare'),
        ('business', 'Business Expenses'),
        ('other', 'Other'),
    ]
    
    TYPE_CHOICES = [
        ('debit', 'Debit'),
        ('credit', 'Credit'),
    ]
    
    document = models.ForeignKey(PDFDocument, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateField()
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    transaction_type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    confidence_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date', '-id']
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['category']),
            models.Index(fields=['transaction_type']),
        ]
    
    def __str__(self):
        return f"{self.date} - {self.description} - ${self.amount}"