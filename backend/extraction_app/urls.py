from django.urls import path
from . import views

urlpatterns = [
    path('upload-pdf/', views.upload_pdf, name='upload_pdf'),
    path('search-transactions/', views.search_transactions, name='search_transactions'),
    path('categories/', views.transaction_categories, name='transaction_categories'),
]