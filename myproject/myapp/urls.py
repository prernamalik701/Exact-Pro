from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('document/<int:document_id>/', views.document_detail, name='document_detail'),
]
