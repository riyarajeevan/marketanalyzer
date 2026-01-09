import pandas as pd
import numpy as np

class ReturnCalculator:
    @staticmethod
    def simple_returns(prices):
        return prices.pct_change().dropna()
    
    @staticmethod
    def log_returns(prices):
        return np.log(prices / prices.shift(1)).dropna()
    
    @staticmethod
    def cumulative_returns(returns):
        return (1 + returns).cumprod() - 1
    
    @staticmethod
    def annualized_return(returns, periods_per_year=252):
        return (1 + returns.mean()) ** periods_per_year - 1


class VolatilityCalculator:
    @staticmethod
    def realized_volatility(returns, periods_per_year=252):
        return returns.std() * np.sqrt(periods_per_year)
    
    @staticmethod
    def rolling_volatility(returns, window=30, periods_per_year=252):
        return returns.rolling(window=window).std() * np.sqrt(periods_per_year)
    
    @staticmethod
    def sharpe_ratio(returns, risk_free_rate=0.0, periods_per_year=252):
        excess_returns = returns - (risk_free_rate / periods_per_year)
        return np.sqrt(periods_per_year) * excess_returns.mean() / returns.std()
    
    @staticmethod
    def max_drawdown(returns):
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.expanding().max()
        drawdown = (cumulative - running_max) / running_max
        return drawdown.min()
    
    @staticmethod
    def var(returns, confidence_level=0.05):
        return returns.quantile(confidence_level)
    
    @staticmethod
    def cvar(returns, confidence_level=0.05):
        var_value = VolatilityCalculator.var(returns, confidence_level)
        return returns[returns <= var_value].mean()
