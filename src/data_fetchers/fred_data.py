"""
FRED (Federal Reserve Economic Data) fetcher.
Requires FRED API key: https://fred.stlouisfed.org/docs/api/api_key.html
"""

import pandas as pd
from typing import Optional, List
from datetime import datetime
import os
from dotenv import load_dotenv

try:
    from fredapi import Fred
except ImportError:
    Fred = None


class FREDFetcher:
    """Fetch economic data from FRED."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize FRED fetcher.
        
        Parameters:
        -----------
        api_key : str, optional
            FRED API key. If not provided, will try to load from .env file
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('FRED_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "FRED API key required. "
                "Get one at https://fred.stlouisfed.org/docs/api/api_key.html "
                "and set FRED_API_KEY in .env file or pass as parameter."
            )
        
        if Fred is None:
            raise ImportError("fredapi package not installed. Run: pip install fredapi")
        
        self.fred = Fred(api_key=self.api_key)
    
    def get_series(
        self,
        series_id: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        frequency: Optional[str] = None
    ) -> pd.Series:
        """
        Fetch a FRED data series.
        
        Parameters:
        -----------
        series_id : str
            FRED series ID (e.g., 'DGS10' for 10-Year Treasury Rate)
        start_date : str, optional
            Start date (format: 'YYYY-MM-DD')
        end_date : str, optional
            End date (format: 'YYYY-MM-DD')
        frequency : str, optional
            Data frequency ('d', 'w', 'm', 'q', 'a')
        
        Returns:
        --------
        pd.Series
            Time series data
        """
        return self.fred.get_series(
            series_id,
            observation_start=start_date,
            observation_end=end_date,
            frequency=frequency
        )
    
    def get_multiple_series(
        self,
        series_ids: List[str],
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Fetch multiple FRED series.
        
        Parameters:
        -----------
        series_ids : List[str]
            List of FRED series IDs
        start_date : str, optional
            Start date
        end_date : str, optional
            End date
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with multiple series as columns
        """
        data = {}
        for series_id in series_ids:
            try:
                data[series_id] = self.get_series(series_id, start_date, end_date)
            except Exception as e:
                print(f"Error fetching {series_id}: {e}")
                continue
        
        return pd.DataFrame(data)
    
    def search_series(self, search_text: str, limit: int = 20) -> pd.DataFrame:
        """
        Search for FRED series.
        
        Parameters:
        -----------
        search_text : str
            Search query
        limit : int
            Maximum number of results
        
        Returns:
        --------
        pd.DataFrame
            Search results
        """
        return self.fred.search(search_text, limit=limit)


# Common FRED series IDs
FRED_SERIES = {
    'DGS10': '10-Year Treasury Rate',
    'DGS2': '2-Year Treasury Rate',
    'DGS30': '30-Year Treasury Rate',
    'DFF': 'Federal Funds Rate',
    'UNRATE': 'Unemployment Rate',
    'CPIAUCSL': 'Consumer Price Index',
    'GDP': 'Gross Domestic Product',
    'VIXCLS': 'VIX Volatility Index',
    'DEXUSEU': 'USD/EUR Exchange Rate',
    'DEXUSUK': 'USD/GBP Exchange Rate',
}

