from django.urls import path
from .views import SignLanguageTranslationView

urlpatterns = [
    path('translate/', SignLanguageTranslationView.as_view(), name='translate'),
]
