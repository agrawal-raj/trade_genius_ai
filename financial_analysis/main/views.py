from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import json 
import os
from django.conf import settings
from .models import Company, Analysis, ProsAndCons
from .services import fetch_all_companies_data, preprocess_companies_data, analyze_companies_data, store_analysis_in_db

# Create your views here.

@api_view(['POST'])
def fetch_companies(request):
    result = fetch_all_companies_data()
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def preprocess_data(request):
    result = preprocess_companies_data()
    return Response(result, status=status.HTTP_200_OK)

@api_view(['POST'])
def analyze_data(request):
    result = analyze_companies_data()
    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_companies(request):
    """Get all companies"""
    companies = Company.objects.all()
    companies_data = []
    
    for company in companies:
        companies_data.append({
            'id': company.id,
            'company_name': company.company_name,
            'company_logo': company.company_logo,
            "about_company": company.about_company,
            "website" : company.website,
            'roe_percentage': float(company.roe_percentage) if company.roe_percentage else None
        })
    
    return Response(companies_data, status=status.HTTP_200_OK)

@api_view(['GET'])
def get_company_analysis(request, company_id):
    analysis_path = os.path.join(settings.BASE_DIR, 'data', 'analysis_data.json')

    if not os.path.exists(analysis_path):
        return Response(
            {"status": "error", "message": "Analysis data not found. Please run analysis first."},
            status=status.HTTP_404_NOT_FOUND
        )
    
    try:
        with open(analysis_path, 'r') as f:
            analysis_data = json.load(f)
        
        # Check if company exists in the analysis data
        if company_id not in analysis_data:
            return Response(
                {"status": "error", "message": f"Company {company_id} not found in analysis data."},
                status=status.HTTP_404_NOT_FOUND
            )
        
        company_analysis = analysis_data[company_id]
        
        # Get additional company info from database (if available)
        try:
            company_db = Company.objects.get(id=company_id)
            company_info = {
                'id': company_db.id,
                'company_name': company_db.company_name,
                'company_logo': company_db.company_logo,
                'about_company': company_db.about_company,
                'website' : company_db.website,
                'roe_percentage': float(company_db.roe_percentage) if company_db.roe_percentage else None
            }
        except Company.DoesNotExist:
            # Use data from JSON if not in database
            company_info = {
                'id': company_id,
                'company_name': company_analysis.get('company_name', company_id),
                'company_logo': None,
                'about_company': None,
                'website': None,
                'roe_percentage': None
            }
        
        # Format the response to match what React expects
        response_data = {
            'company': company_info,
            'analysis': company_analysis.get('analysis', {}),
            'pros': company_analysis.get('pros', []),
            'cons': company_analysis.get('cons', [])
        }
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {"status": "error", "message": f"Error reading analysis data: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
   
@api_view(['POST'])
def analyze_and_store_data(request):
    analyze_result = analyze_companies_data()

    if analyze_result.get('status') != 'success':
        return Response(analyze_result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    analysis_path = os.path.join(settings.BASE_DIR, 'data', 'analysis_data.json')

    if not os.path.exists(analysis_path):
        return Response({"status": "error", "message": "Analysis data not found."},
                        status=status.HTTP_404_NOT_FOUND)
    
    with open(analysis_path, 'r') as f:
        analysis_data = json.load(f)

    store_result = store_analysis_in_db(analysis_data)

    if store_result.get('status') != 'success':
        return Response(store_result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response({"status": "success", "message": "Data analyzed and stored in database successfully"})