"""
Alpha Vantage data fetcher.
Requires Alpha Vantage API key: https://www.alphavantage.co/support/#api-key
Free tier: 5 API calls per minute, 500 calls per day
"""

import pandas as pd
from typing import Optional, Dict
import os
from dotenv import load_dotenv
import time

try:
    from alpha_vantage.timeseries import TimeSeries
    from alpha_vantage.techindicators import TechIndicators
except ImportError:
    TimeSeries = None
    TechIndicators = None


class AlphaVantageFetcher:
    """Fetch data from Alpha Vantage API."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Alpha Vantage fetcher.
        
        Parameters:
        -----------
        api_key : str, optional
            Alpha Vantage API key. If not provided, will try to load from .env file
        """
        load_dotenv()
        self.api_key = api_key or os.getenv('ALPHA_VANTAGE_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "Alpha Vantage API key required. "
                "Get one at https://www.alphavantage.co/support/#api-key "
                "and set ALPHA_VANTAGE_API_KEY in .env file or pass as parameter."
            )
        
        if TimeSeries is None:
            raise ImportError("alpha-vantage package not installed. Run: pip install alpha-vantage")
        
        self.ts = TimeSeries(key=self.api_key, output_format='pandas')
        self.ti = TechIndicators(key=self.api_key, output_format='pandas')
        self.last_call_time = 0
        self.min_call_interval = 12  # 5 calls per minute = 12 seconds between calls
    
    def _rate_limit(self):
        """Enforce rate limiting (5 calls per minute)."""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        
        if time_since_last_call < self.min_call_interval:
            sleep_time = self.min_call_interval - time_since_last_call
            time.sleep(sleep_time)
        
        self.last_call_time = time.time()
    
    def get_stock_data(
        self,
        symbol: str,
        interval: str = 'daily',
        outputsize: str = 'compact'
    ) -> pd.DataFrame:
        """
        Fetch stock time series data.
        
        Parameters:
        -----------
        symbol : str
            Stock ticker symbol
        interval : str
            Time interval ('1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly')
        outputsize : str
            'compact' (last 100 data points) or 'full' (full historical data)
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with OHLCV data
        """
        self._rate_limit()
        
        if interval == 'daily':
            data, meta = self.ts.get_daily(symbol=symbol, outputsize=outputsize)
        elif interval == 'weekly':
            data, meta = self.ts.get_weekly(symbol=symbol)
        elif interval == 'monthly':
            data, meta = self.ts.get_monthly(symbol=symbol)
        else:
            data, meta = self.ts.get_intraday(symbol=symbol, interval=interval, outputsize=outputsize)
        
        # Rename columns to lowercase
        data.columns = [col.split('. ')[1].lower().replace(' ', '_') for col in data.columns]
        
        return data
    
    def get_technical_indicator(
        self,
        symbol: str,
        indicator: str,
        interval: str = 'daily',
        **kwargs
    ) -> pd.DataFrame:
        """
        Get technical indicators.
        
        Parameters:
        -----------
        symbol : str
            Stock ticker symbol
        indicator : str
            Indicator name ('SMA', 'EMA', 'RSI', 'MACD', 'BBANDS', 'STOCH', etc.)
        interval : str
            Time interval
        **kwargs
            Additional parameters for the indicator
        
        Returns:
        --------
        pd.DataFrame
            DataFrame with indicator values
        """
        self._rate_limit()
        
        indicator_map = {
            'SMA': self.ti.get_sma,
            'EMA': self.ti.get_ema,
            'RSI': self.ti.get_rsi,
            'MACD': self.ti.get_macd,
            'BBANDS': self.ti.get_bbands,
            'STOCH': self.ti.get_stoch,
        }
        
        if indicator not in indicator_map:
            raise ValueError(f"Indicator {indicator} not supported. Available: {list(indicator_map.keys())}")
        
        func = indicator_map[indicator]
        data, meta = func(symbol=symbol, interval=interval, **kwargs)
        
        return data

