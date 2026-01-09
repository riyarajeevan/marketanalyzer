import yfinance as yf

class YahooFinanceFetcher:
    def __init__(self):
        pass
    
    def get_stock_data(self, ticker, start_date=None, end_date=None, period="1y", interval="1d"):
        stock = yf.Ticker(ticker)
        
        if start_date and end_date:
            data = stock.history(start=start_date, end=end_date, interval=interval)
        else:
            data = stock.history(period=period, interval=interval)
        
        data.columns = [col.lower().replace(' ', '_') for col in data.columns]
        
        return data
    
    def get_multiple_stocks(self, tickers, start_date=None, end_date=None, period="1y"):
        if start_date and end_date:
            data = yf.download(tickers, start=start_date, end=end_date, progress=False)
        else:
            data = yf.download(tickers, period=period, progress=False)
        
        return data
    
    def get_stock_info(self, ticker):
        stock = yf.Ticker(ticker)
        return stock.info
    
    def get_dividends(self, ticker):
        stock = yf.Ticker(ticker)
        return stock.dividends.to_frame(name='dividend')
    
    def get_splits(self, ticker):
        stock = yf.Ticker(ticker)
        return stock.splits.to_frame(name='split')
