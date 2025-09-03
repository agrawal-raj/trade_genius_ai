from django.db import transaction
from .models import Company, Analysis, ProsAndCons
from django.utils import timezone 
import os
import json
import pandas as pd
import requests
import time
from django.conf import settings
import logging
from typing import Dict, List, Optional
import re
import numpy as np



def ensure_directory_exists(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_all_company_ids(file_path):
    try:
        df = pd.read_excel(file_path)
        company_ids = df['company_id'].str.strip().tolist()
        print(f"Successfully read {len(company_ids)} company IDs from Excel.")
        return company_ids
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return []

def fetch_financial_data(company_id, api_key):
    url = "https://bluemutualfund.in/server/api/company.php"
    params = {
        'id': company_id,
        'api_key': api_key
    }
    try:
        print(f"Fetching data for {company_id}...")
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Successfully fetched data for {company_id}")
                return data
            except json.JSONDecodeError:
                print(f"Error: Response for {company_id} is not valid JSON.")
                return None
        else:
            print(f"Error: Failed to fetch {company_id} (Status Code: {response.status_code})")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Network error for {company_id}: {e}")
        return None

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FinancialDataPreprocessor:
    def __init__(self):
        self.standardized_keys = {
            # Company info mappings
            'company_name': ['company_name', 'name', 'Name'],
            'company_logo': ['company_logo', 'logo', 'Logo'],
            'about_company': ['about_company', 'about', 'description', 'Description'],
            'website':['website', 'url', 'Website'], 
            'face_value': ['face_value', 'facevalue', 'FV'],
            'book_value': ['book_value', 'bookvalue', 'BV'],
            'roce_percentage': ['roce_percentage', 'roce', 'ROCE'],
            'roe_percentage': ['roe_percentage', 'roe', 'ROE'],
            
            # Financial statement mappings
            'sales': ['sales', 'revenue', 'total_revenue'],
            'net_profit': ['net_profit', 'netprofit', 'profit_after_tax', 'PAT'],
            'operating_profit': ['operating_profit', 'op_profit', 'EBIT'],
            'borrowings': ['borrowings', 'debt', 'total_debt', 'loans'],
            'equity_capital': ['equity_capital', 'share_capital', 'paid_up_capital'],
            'reserves': ['reserves', 'reserves_surplus'],
            'dividend_payout': ['dividend_payout', 'div_payout', 'payout_ratio'],
            'eps': ['eps', 'earnings_per_share', 'EPS']
        }
    
    def load_data(self, file_path: str) -> Dict:
        """Load JSON data from file"""
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            logger.info(f"Successfully loaded data with {len(data)} companies")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return {}
    
    def standardize_key_names(self, data_dict: Dict) -> Dict:
        """Standardize key names across all companies"""
        standardized_data = {}
        
        for company_id, company_data in data_dict.items():
            standardized_company = {}
            
            # Standardize company info
            if 'company' in company_data:
                standardized_company['company'] = self._standardize_dict(company_data['company'])
            
            # Standardize data sections
            if 'data' in company_data:
                standardized_data_section = {}
                for section, items in company_data['data'].items():
                    if isinstance(items, list):
                        standardized_data_section[section] = [
                            self._standardize_dict(item) for item in items
                        ]
                    else:
                        standardized_data_section[section] = items
                standardized_company['data'] = standardized_data_section
            
            standardized_data[company_id] = standardized_company
            print("Test data", standardized_data[company_id])
        
        return standardized_data
    
    def _standardize_dict(self, data_dict: Dict) -> Dict:
        """Standardize keys in a single dictionary"""
        standardized = {}
        for key, value in data_dict.items():
            standardized_key = self._find_standard_key(key)
            standardized[standardized_key] = value
        return standardized
    
    def _find_standard_key(self, key: str) -> str:
        """Find the standard key name for a given key"""
        for standard_key, variations in self.standardized_keys.items():
            if key in variations:
                return standard_key
        return key  # Return original if no standardization found
    
    def convert_strings_to_float(self, data_dict: Dict) -> Dict:
        """Convert numeric strings to float values"""
        processed_data = {}
        
        for company_id, company_data in data_dict.items():
            processed_company = {}
            
            if 'company' in company_data:
                processed_company['company'] = self._convert_dict_values(company_data['company'])
            
            if 'data' in company_data:
                processed_data_section = {}
                for section, items in company_data['data'].items():
                    if isinstance(items, list):
                        processed_data_section[section] = [
                            self._convert_dict_values(item) for item in items
                        ]
                    else:
                        processed_data_section[section] = items
                processed_company['data'] = processed_data_section
            
            processed_data[company_id] = processed_company
        
        return processed_data
    
    def _convert_dict_values(self, data_dict: Dict) -> Dict:
        """Convert numeric values in a dictionary to float"""
        converted = {}
        for key, value in data_dict.items():
            if isinstance(value, str):
                # Handle percentage values
                if '%' in str(value):
                    converted_value = self._parse_percentage(value)
                else:
                    converted_value = self._parse_numeric(value)
                converted[key] = converted_value
            else:
                converted[key] = value
        return converted
    
    def _parse_numeric(self, value: str) -> Optional[float]:
        """Parse numeric string to float, handling various formats"""
        if value is None or value == '' or value == 'null' or value == 'None':
            return None
        
        # Remove commas and extra spaces
        cleaned = str(value).replace(',', '').strip()
        
        # Handle negative numbers in parentheses
        if cleaned.startswith('(') and cleaned.endswith(')'):
            cleaned = '-' + cleaned[1:-1]
        
        try:
            return float(cleaned)
        except (ValueError, TypeError):
            logger.warning(f"Could not convert '{value}' to float")
            return None
    
    def _parse_percentage(self, value: str) -> Optional[float]:
        """Parse percentage string to float"""
        if value is None:
            return None
        
        # Extract numeric part
        numeric_part = re.sub(r'[^\d.-]', '', str(value))
        try:
            return float(numeric_part)
        except (ValueError, TypeError):
            logger.warning(f"Could not parse percentage '{value}'")
            return None
    
    def remove_invalid_entries(self, data_dict: Dict, min_valid_years: int = 5) -> Dict:
        """Remove companies with insufficient or invalid data"""
        valid_companies = {}
        removed_count = 0
        
        for company_id, company_data in data_dict.items():
            if self._is_valid_company(company_data, min_valid_years):
                valid_companies[company_id] = company_data
            else:
                removed_count += 1
                logger.info(f"Removed company {company_id} due to insufficient data")
        
        logger.info(f"Removed {removed_count} companies, kept {len(valid_companies)}")
        return valid_companies
    
    def _is_valid_company(self, company_data: Dict, min_valid_years: int) -> bool:
        """Check if a company has sufficient valid data"""
        # Check basic company info
        if 'company' not in company_data:
            return False
        
        company_info = company_data['company']

        if 'company_name' not in company_info:
            return False

        # if not all(key in company_info for key in ['company_name', 'roe_percentage']):
        #     return False
        
        # Check financial data existence
        if 'data' not in company_data:
            return False
        
        data_section = company_data['data']
        
        has_some_financial_data = (
            'profitandloss' in data_section or
            'balancesheet' in data_section or
            'cashflow' in data_section
        )

        return has_some_financial_data or len(company_info) > 1
        # Check for sufficient profit and loss data
        # if 'profitandloss' not in data_section or len(data_section['profitandloss']) < min_valid_years:
        #     return False
        
        # # Check for sufficient balance sheet data
        # if 'balancesheet' not in data_section or len(data_section['balancesheet']) < min_valid_years:
        #     return False
        
        # return True
    
    def remove_null_fields(self, data_dict: Dict) -> Dict:
        """Remove fields with null, empty, or invalid values"""
        cleaned_data = {}
        
        for company_id, company_data in data_dict.items():
            cleaned_company = {}
            
            if 'company' in company_data:
                cleaned_company['company'] = self._clean_dict(company_data['company'])
            
            if 'data' in company_data:
                cleaned_data_section = {}
                for section, items in company_data['data'].items():
                    if isinstance(items, list):
                        cleaned_data_section[section] = [
                            self._clean_dict(item) for item in items
                        ]
                    else:
                        cleaned_data_section[section] = items
                cleaned_company['data'] = cleaned_data_section
            
            cleaned_data[company_id] = cleaned_company
        
        return cleaned_data
    
    def _clean_dict(self, data_dict: Dict) -> Dict:
        """Remove null/empty fields from a dictionary, but keep important company info"""
        cleaned = {}
        for k, v in data_dict.items():
            # For company info, be more lenient about what we keep
            if k in ['company_name', 'company_logo', 'about_company', 'website', 
                    'nse_profile', 'bse_profile', 'chart_link']:
                # Keep these fields even if they're empty strings
                if v is not None and v != 'null' and v != 'None' and not pd.isna(v):
                    cleaned[k] = v
            else:
                # For other fields, use the original strict logic
                if v not in [None, '', 'null', 'None', 'NaN', 'nan'] and not pd.isna(v):
                    cleaned[k] = v
        return cleaned
        # return {k: v for k, v in data_dict.items() 
        #         if v not in [None, '', 'null', 'None', 'NaN', 'nan'] and not pd.isna(v)}
    
    def log_preprocessed_data(self, data_dict: Dict, sample_size: int = 3):
        """Log sample of preprocessed data for inspection"""
        logger.info("=== PREPROCESSED DATA SAMPLE ===")
        
        sample_companies = list(data_dict.keys())[:sample_size]
        
        for company_id in sample_companies:
            company_data = data_dict[company_id]
            logger.info(f"\nCompany: {company_id}")
            
            if 'company' in company_data:
                logger.info(f"Company Info: {list(company_data['company'].keys())}")
            
            if 'data' in company_data:
                data_section = company_data['data']
                for section, items in data_section.items():
                    if isinstance(items, list) and items:
                        logger.info(f"{section}: {len(items)} records")
                        if section == 'profitandloss':
                            # Show latest financial metrics
                            latest = items[-1]
                            logger.info(f"Latest {section}: { {k: v for k, v in list(latest.items())[:5]} }...")
    
    def get_data_summary(self, data_dict: Dict) -> Dict:
        """Get summary statistics of the preprocessed data"""
        summary = {
            'total_companies': len(data_dict),
            'companies_with_sufficient_data': 0,
            'average_years_data': 0,
            'common_metrics': {}
        }
        
        total_years = 0
        metric_counts = {}
        
        for company_id, company_data in data_dict.items():
            if 'data' in company_data and 'profitandloss' in company_data['data']:
                pl_data = company_data['data']['profitandloss']
                total_years += len(pl_data)
                summary['companies_with_sufficient_data'] += 1
                
                # Count available metrics
                if pl_data:
                    for metric in pl_data[0].keys():
                        metric_counts[metric] = metric_counts.get(metric, 0) + 1
        
        if summary['companies_with_sufficient_data'] > 0:
            summary['average_years_data'] = total_years / summary['companies_with_sufficient_data']
        
        summary['common_metrics'] = metric_counts
        return summary

# Main preprocessing function
def preprocess_financial_data(file_path: str, min_valid_years: int = 5) -> Dict:
    """Complete preprocessing pipeline"""
    preprocessor = FinancialDataPreprocessor()
    
    # Load data
    raw_data = preprocessor.load_data(file_path)
    if not raw_data:
        return {}
    
    logger.info("Starting data preprocessing...")

    #debug point
    sample_company_id = list(raw_data.keys())[0] if raw_data else None
    if sample_company_id and 'company' in raw_data[sample_company_id]:
        logger.info(f'Sample company data before processing: {list(raw_data[sample_company_id] ['company'].keys())}')
    
    # Step 1: Standardize key names
    standardized_data = preprocessor.standardize_key_names(raw_data)
    logger.info("Step 1: Key names standardized")

    #debug point
    if sample_company_id and sample_company_id in standardized_data and 'company' in standardized_data[sample_company_id]:
        logger.info(f"Sample company data after standardization: {list(standardized_data[sample_company_id]['company'].keys())}")
    
    # Step 2: Convert strings to numeric values
    numeric_data = preprocessor.convert_strings_to_float(standardized_data)
    logger.info("Step 2: Numeric conversion completed")
    
    # Step 3: Remove invalid entries
    valid_data = preprocessor.remove_invalid_entries(numeric_data, min_valid_years)
    logger.info("Step 3: Invalid entries removed")
    
    # Step 4: Remove null fields
    cleaned_data = preprocessor.remove_null_fields(valid_data)
    logger.info("Step 4: Null fields removed")
    
    #debug
    if sample_company_id and sample_company_id in cleaned_data and 'company' in cleaned_data[sample_company_id]:
        logger.info(f"Sample company data after cleaning: {list(cleaned_data[sample_company_id]['company'].keys())}") 

    # Log results
    preprocessor.log_preprocessed_data(cleaned_data)
    summary = preprocessor.get_data_summary(cleaned_data)
    logger.info(f"Data Summary: {summary}")
    
    return cleaned_data


#pros_cons_data 
class FinancialAnalyzer:
    def __init__(self):
        self.pros_templates = {
            'debt_free': "Company is almost debt-free.",
            'debt_reduced': "Company has reduced debt.",
            'good_roe': "Company has a good return on equity (ROE) track record: {period} Years ROE {value:.1f}%",
            'healthy_dividend': "Company has been maintaining a healthy dividend payout of {value:.1f}%",
            'good_profit_growth': "Company has delivered good profit growth of {value:.1f}% over past {period} years",
            'good_sales_growth': "Company has delivered good sales growth of {value:.1f}% over past {period} years"
        }
        
        self.cons_templates = {
            'poor_sales_growth': "The company has delivered a poor sales growth of {value:.1f}% over past {period} years.",
            'no_dividend': "Company is not paying out dividend.",
            'low_roe': "Company has a low return on equity of {value:.1f}% over last {period} years.",
            'poor_profit_growth': "The company has delivered a poor profit growth of {value:.1f}% over past {period} years.",
            'high_debt': "Company has high debt levels with debt-to-equity ratio of {value:.1f}%"
        }

    def calculate_cagr(self, values: List[float], years: int) -> Optional[float]:
        """Calculate Compound Annual Growth Rate"""
        if len(values) < years or years <= 0:
            return None
        
        start_value = values[-years]
        end_value = values[-1]
        
        if start_value <= 0 or end_value <= 0:
            return None
            
        cagr = (end_value / start_value) ** (1/years) - 1
        return cagr * 100

    def calculate_average_roe(self, profit_data: List[Dict], balance_data: List[Dict], years: int) -> Optional[float]:
        """Calculate average Return on Equity over specified period"""
        if len(profit_data) < years or len(balance_data) < years:
            return None
        
        roe_values = []
        for i in range(1, years + 1):
            if -i < -len(profit_data) or -i < -len(balance_data):
                break
                
            net_profit = profit_data[-i].get('net_profit')
            equity = balance_data[-i].get('reserves', 0) + balance_data[-i].get('equity_capital', 0)
            
            if net_profit is not None and equity is not None and equity > 0:
                roe = (net_profit / equity) * 100
                roe_values.append(roe)
        
        return np.mean(roe_values) if roe_values else None

    def analyze_company(self, company_id: str, company_data: Dict) -> Dict:
        """Complete analysis for a single company with API-ready JSON structure"""
        
        company_info = company_data.get('company', {})

        result = {
            "company_id": company_id,
            "company_info": company_info,
            "company_name" : company_info.get('company_name', company_id),
            # "company_name": company_data.get('company', {}).get('company_name', company_id),
            "analysis": {
                "compounded_sales_growth": {"3_years": None, "5_years": None, "10_years": None},
                "compounded_profit_growth": {"3_years": None, "5_years": None, "10_years": None},
                "return_on_equity": {"3_years": None, "5_years": None, "10_years": None},
                "debt_analysis": {
                    "current_debt": 0,
                    "current_equity": 0,
                    "debt_to_equity_ratio": 0,
                    "debt_trend": "unknown"
                },
                "dividend_analysis": {
                    "current_dividend_payout": 0,
                    "dividend_status": "unknown"
                }
            },
            "pros": [],
            "cons": [],
            "status": "success"
        }
        
        try:
            # Extract financial data
            profit_data = company_data.get('data', {}).get('profitandloss', [])
            balance_data = company_data.get('data', {}).get('balancesheet', [])
            
            if not profit_data or not balance_data:
                result["status"] = "insufficient_data"
                return result
            
            # Extract time series data
            sales = [item.get('sales', 0) for item in profit_data if item.get('sales') is not None]
            profits = [item.get('net_profit', 0) for item in profit_data if item.get('net_profit') is not None]
            dividends = [item.get('dividend_payout', 0) for item in profit_data if item.get('dividend_payout') is not None]
            debts = [item.get('borrowings', 0) for item in balance_data if item.get('borrowings') is not None]
            
            # Get latest values
            latest_balance = balance_data[-1] if balance_data else {}
            latest_profit = profit_data[-1] if profit_data else {}
            
            current_debt = latest_balance.get('borrowings', 0) or 0
            current_equity = (latest_balance.get('reserves', 0) or 0) + (latest_balance.get('equity_capital', 0) or 0)
            current_dividend = latest_profit.get('dividend_payout', 0) or 0
            debt_ratio = (current_debt / current_equity * 100) if current_equity > 0 else 100
            
            # Calculate growth metrics
            for years in [3, 5, 10]:
                sales_growth = self.calculate_cagr(sales, years)
                profit_growth = self.calculate_cagr(profits, years)
                roe = self.calculate_average_roe(profit_data, balance_data, years)
                
                # Add to analysis
                result["analysis"]["compounded_sales_growth"][f"{years}_years"] = round(sales_growth, 2) if sales_growth else None
                result["analysis"]["compounded_profit_growth"][f"{years}_years"] = round(profit_growth, 2) if profit_growth else None
                result["analysis"]["return_on_equity"][f"{years}_years"] = round(roe, 2) if roe else None
            
            # Debt analysis
            result["analysis"]["debt_analysis"] = {
                "current_debt": round(float(current_debt), 2),
                "current_equity": round(float(current_equity), 2),
                "debt_to_equity_ratio": round(float(debt_ratio), 2),
                "debt_trend": "decreasing" if len(debts) > 1 and current_debt < debts[-2] else "stable" if len(debts) > 1 and current_debt == debts[-2] else "increasing"
            }
            
            # Dividend analysis
            result["analysis"]["dividend_analysis"] = {
                "current_dividend_payout": round(float(current_dividend), 2),
                "dividend_status": "paying" if current_dividend and current_dividend > 0 else "not_paying"
            }
            
            # Generate pros and cons
            result["pros"] = self.generate_pros(result["analysis"], current_debt, current_equity, current_dividend, debts)
            result["cons"] = self.generate_cons(result["analysis"], current_debt, current_equity, current_dividend)
            
            # Select top 3 pros and cons
            result["pros"] = result["pros"][:3]
            result["cons"] = result["cons"][:3]
            
        except Exception as e:
            result["status"] = f"error: {str(e)}"
        
        return result

    def generate_pros(self, analysis: Dict, current_debt: float, current_equity: float, 
                     current_dividend: float, debt_history: List[float]) -> List[str]:
        """Generate positive insights"""
        pros = []
        
        # Debt analysis
        debt_ratio = (current_debt / current_equity * 100) if current_equity > 0 else 100
        if debt_ratio < 5:
            pros.append(self.pros_templates['debt_free'])
        
        # Debt reduction
        if len(debt_history) >= 2 and current_debt < debt_history[-2]:
            pros.append(self.pros_templates['debt_reduced'])
        
        # ROE analysis
        for years in [3, 5]:
            roe = analysis["return_on_equity"].get(f"{years}_years")
            if roe and roe > 15:
                pros.append(self.pros_templates['good_roe'].format(period=years, value=roe))
        
        # Dividend analysis
        if current_dividend and current_dividend > 30:
            pros.append(self.pros_templates['healthy_dividend'].format(value=current_dividend))
        
        # Profit growth analysis
        for years in [3, 5]:
            growth = analysis["compounded_profit_growth"].get(f"{years}_years")
            if growth and growth > 15:
                pros.append(self.pros_templates['good_profit_growth'].format(value=growth, period=years))
        
        # Sales growth analysis
        for years in [3, 5]:
            growth = analysis["compounded_sales_growth"].get(f"{years}_years")
            if growth and growth > 15:
                pros.append(self.pros_templates['good_sales_growth'].format(value=growth, period=years))
        
        return pros

    def generate_cons(self, analysis: Dict, current_debt: float, current_equity: float, 
                     current_dividend: float) -> List[str]:
        """Generate negative insights"""
        cons = []
        
        # Debt analysis
        debt_ratio = (current_debt / current_equity * 100) if current_equity > 0 else 100
        if debt_ratio > 50:
            cons.append(self.cons_templates['high_debt'].format(value=debt_ratio))
        
        # Dividend analysis
        if not current_dividend or current_dividend == 0:
            cons.append(self.cons_templates['no_dividend'])
        
        # ROE analysis
        for years in [3, 5]:
            roe = analysis["return_on_equity"].get(f"{years}_years")
            if roe and roe < 10:
                cons.append(self.cons_templates['low_roe'].format(value=roe, period=years))
        
        # Sales growth analysis
        for years in [3, 5]:
            growth = analysis["compounded_sales_growth"].get(f"{years}_years")
            if growth and growth < 10:
                cons.append(self.cons_templates['poor_sales_growth'].format(value=growth, period=years))
        
        # Profit growth analysis
        for years in [3, 5]:
            growth = analysis["compounded_profit_growth"].get(f"{years}_years")
            if growth and growth < 10:
                cons.append(self.cons_templates['poor_profit_growth'].format(value=growth, period=years))
        
        return cons

def generate_complete_analysis(processed_data_path: str) -> Dict:
    """Generate complete analysis JSON for all companies"""
    
    try:
        with open(processed_data_path, 'r') as f:
            processed_data = json.load(f)
    except FileNotFoundError:
        return {"error": "Processed data file not found", "status": "error"}
    
    analyzer = FinancialAnalyzer()
    analysis_results = {}
    
    for company_id, company_data in processed_data.items():
        result = analyzer.analyze_company(company_id, company_data)
        analysis_results[company_id] = result
    
    return analysis_results

def store_analysis_in_db(analysis_results):
    try:
        with transaction.atomic():
            for company_id, company_data in analysis_results.items():

                company_info = company_data.get('company_info', {})
                company, created = Company.objects.update_or_create(
                    id=company_id,
                    defaults = {
                        'company_name' : company_info.get('company_name', ''),
                        'company_logo' : company_info.get('company_logo'),
                        'about_company': company_info.get('about_company'),
                        'website' : company_info.get('website'),
                        'roce_percentage': company_info.get('roce_percentage'),
                        'roe_percentage' : company_info.get('roe_percentage'),
                    }
                )

                analysis = company_data.get('analysis', {})

                sales_growth = analysis.get('compounded_sales_growth', {})
                profit_growth = analysis.get('compounded_sales_growth', {})
                roe_data = analysis.get('return_on_equity', {})

                for years in [3, 5, 10]:
                    sales_key = f"{years}_years"
                    profit_key = f"{years}_years"
                    roe_key = f"{years}_years"

                    if sales_key in sales_growth or profit_key in profit_growth or roe_key in roe_data:
                        analysis_id = f"{company_id[:45]}_{years}"

                        Analysis.objects.update_or_create(
                            id = analysis_id,
                            defaults = {
                                'company_id' : company_id,
                                'compounded_sales_growth': f"{years} Years: {sales_growth.get(sales_key, 'N/A')}%",
                                'compounded_profit_growth' : f"{years} Years: {profit_growth.get(profit_key, 'N/A')}%",
                                'stock_price_cagr': f"{years} Years: N/A", 
                                'roe': f"{years} Years: {roe_data.get(roe_key, 'N/A')}%",
                            }
                        )
                pros = company_data.get('pros', [])
                cons = company_data.get('cons', [])

                ProsAndCons.objects.filter(company_id= company_id).delete()

                for pro in pros[:3]:
                    ProsAndCons.objects.create(
                        company_id = company_id,
                        pros = pro,
                        cons = None
                    )

                for con in cons[:3]:
                    ProsAndCons.objects.create(
                        company_id= company_id,
                        pros = None,
                        cons =con
                    )

            return {"status": "success", "message": "Data stored in database successfully"}
    except Exception as e:
        return {"status": "error", "message":f"Error storing data in database: {str(e)}"}


# Service functions for the API
def fetch_all_companies_data():
    API_KEY = "ghfkffu6378382826hhdjgk"
    EXCEL_FILE_PATH = os.path.join(settings.BASE_DIR, 'data', 'company_id.xlsx')
    OUTPUT_FILE_PATH = os.path.join(settings.BASE_DIR, 'data', 'all_companies_financial_data.json')
    
    all_company_ids = get_all_company_ids(EXCEL_FILE_PATH)
    
    if not all_company_ids:
        return {"status": "error", "message": "No company IDs to process."}
    
    all_financial_data = {}
    
    for company_id in all_company_ids:
        financial_data = fetch_financial_data(company_id, API_KEY)
        if financial_data:
            all_financial_data[company_id] = financial_data
        time.sleep(1)
    
    # Save data to file
    with open(OUTPUT_FILE_PATH, 'w') as json_file:
        json.dump(all_financial_data, json_file, indent=2)
    
    return {"status": "success", "message": f"Successfully retrieved data for {len(all_financial_data)} companies."}


def preprocess_companies_data():
    INPUT_FILE_PATH = os.path.join(settings.BASE_DIR, 'data', 'all_companies_financial_data.json')
    OUTPUT_FILE_PATH = os.path.join(settings.BASE_DIR, 'data', 'processed_financial_data.json')
    
    ensure_directory_exists(INPUT_FILE_PATH)
    ensure_directory_exists(OUTPUT_FILE_PATH)

    if not os.path.exists(INPUT_FILE_PATH):
        return{"status": "error", "message": "Input file not found. Please run fetch-companies first."}
    
    processed_data = preprocess_financial_data(INPUT_FILE_PATH, min_valid_years=5)
    
    # Save processed data
    with open(OUTPUT_FILE_PATH, "w") as f:
        json.dump(processed_data, f, indent=2)
    

    return {"status": "success", "message": "Data preprocessing completed."}

def analyze_companies_data():
    INPUT_FILE_PATH = os.path.join(settings.BASE_DIR, 'data', 'processed_financial_data.json')
    OUTPUT_FILE_PATH = os.path.join(settings.BASE_DIR, 'data', 'analysis_data.json')
    
    ensure_directory_exists(INPUT_FILE_PATH)
    ensure_directory_exists(OUTPUT_FILE_PATH)
    
    # Check if input file exists
    if not os.path.exists(INPUT_FILE_PATH):
        return {"status": "error", "message": "Processed data not found. Please run preprocess-data first."}

    analysis_results = generate_complete_analysis(INPUT_FILE_PATH)
    
    # Save analysis results
    with open(OUTPUT_FILE_PATH, 'w') as f:
        json.dump(analysis_results, f, indent=2)
    
    return {"status": "success", "message": "Data analysis completed."}