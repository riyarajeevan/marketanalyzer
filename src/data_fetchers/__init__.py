"""
Data fetching modules for various financial data sources.
"""

from .yahoo_finance import YahooFinanceFetcher

# Make these optional imports - they might not be available if dependencies aren't installed
# Catch any exception, not just ImportError, because the module might fail during import
try:
    from .fred_data import FREDFetcher
except (ImportError, ValueError, Exception):
    FREDFetcher = None

try:
    from .alpha_vantage import AlphaVantageFetcher
except (ImportError, ValueError, Exception):
    AlphaVantageFetcher = None

__all__ = ['YahooFinanceFetcher']
if FREDFetcher is not None:
    __all__.append('FREDFetcher')
if AlphaVantageFetcher is not None:
    __all__.append('AlphaVantageFetcher')

