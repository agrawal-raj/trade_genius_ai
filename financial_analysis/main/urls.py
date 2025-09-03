from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.get_companies, name='get_companies'),
    path('companies/<str:company_id>/analysis/', views.get_company_analysis, name='get_company_analysis'),
    path('fetch-companies/', views.fetch_companies, name ='fetch-companies'),
    path('preprocess-data/', views.preprocess_data, name='preprocess-data'),
    path('analyze-data/', views.analyze_data, name='analyze-data'),
    # path('get-analysis/', views.get_analysis, name='get-analysis'),
    # path('get-analysis/<str:company_id>/', views.get_company_analysis, name='get-company-analysis'),
    path('analyze-and-store/', views.analyze_and_store_data, name='analyze-and-store'),
]
