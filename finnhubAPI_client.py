""" finnhubAPI_client.py - FINNHUB API CLIENT """

import os
from dotenv import load_dotenv
import finnhub

load_dotenv()

FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
if not FINNHUB_API_KEY:
    raise ValueError("API klíč pro Finnhub není definován v .env souboru!")

class FinnhubAPIClient:
    def __init__(self, api_key=None):        
        self.api_key = api_key or FINNHUB_API_KEY
        self.client = finnhub.Client(self.api_key)     

    def get_company_profile(self, symbol: str) -> dict:
        """ Gets the company profile from the Finnhub API based on the ticker """
        try:            
            company_profile = self.client.company_profile2(symbol=symbol)            
            if not company_profile or 'name' not in company_profile:
                return {"error": "❌ Společnost nenalezena nebo chybí data."}            
            return company_profile

        except Exception as e:
            return {"error": f"Chyba při načítání profilu: {str(e)}"}
        
if __name__=="__main__":      
    client = FinnhubAPIClient()
    ticker = "MSFT"
    profile = client.get_company_profile(ticker)
    
    if 'error' in profile:
        print(profile['error'])
    else:
        print(profile)