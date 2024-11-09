# translation_app/urls.py

# translation_app/urls.py

from django.urls import path
from .views import (
    LanguagesView,
    SpecialitiesView,
    StylesView,
    ComplexityLevelsView,
    ModelsView,
    TranslateView,
    ImportDocumentView,
    ExportDocumentView,
)

urlpatterns = [
    path('languages/', LanguagesView.as_view(), name='languages'),
    path('specialities/', SpecialitiesView.as_view(), name='specialities'),
    path('styles/', StylesView.as_view(), name='styles'),
    path('complexity-levels/', ComplexityLevelsView.as_view(), name='complexity_levels'),
    path('models/', ModelsView.as_view(), name='models'),
    path('translate/', TranslateView.as_view(), name='translate'),
    path('import-document/', ImportDocumentView.as_view(), name='import_document'),
    path('export-document/', ExportDocumentView.as_view(), name='export_document'),
]
