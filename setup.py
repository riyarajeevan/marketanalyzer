"""
Setup script to verify installation and test data fetching.
"""

import sys
import os

def check_dependencies():
    """Check if all required packages are installed."""
    print("Checking dependencies...")
    required_packages = [
        'yfinance', 'pandas', 'numpy', 'matplotlib', 
        'seaborn', 'scipy', 'sklearn'
    ]
    
    missing = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                __import__('sklearn')
            else:
                __import__(package)
            print(f"  [OK] {package}")
        except ImportError:
            print(f"  [MISSING] {package}")
            missing.append(package)
    
    if missing:
        print(f"\nMissing packages: {', '.join(missing)}")
        print("Install them with: pip install -r requirements.txt")
        return False
    
    print("\nAll dependencies installed!")
    return True


def test_yahoo_finance():
    """Test Yahoo Finance data fetching."""
    print("\n" + "=" * 60)
    print("Testing Yahoo Finance data fetching...")
    print("=" * 60)
    
    try:
        from src.data_fetchers import YahooFinanceFetcher
        
        fetcher = YahooFinanceFetcher()
        data = fetcher.get_stock_data('AAPL', period='5d')
        
        if data.empty:
            print("  [FAILED] No data returned")
            return False
        
        print(f"  [OK] Successfully fetched {len(data)} rows of AAPL data")
        print(f"  [OK] Columns: {', '.join(data.columns)}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def test_data_processing():
    """Test data processing utilities."""
    print("\n" + "=" * 60)
    print("Testing data processing utilities...")
    print("=" * 60)
    
    try:
        from src.data_fetchers import YahooFinanceFetcher
        from src.data_processing import ReturnCalculator, VolatilityCalculator
        
        fetcher = YahooFinanceFetcher()
        data = fetcher.get_stock_data('AAPL', period='1mo')
        
        calc = ReturnCalculator()
        returns = calc.simple_returns(data['close'])
        
        risk_calc = VolatilityCalculator()
        vol = risk_calc.realized_volatility(returns)
        sharpe = risk_calc.sharpe_ratio(returns)
        
        print(f"  [OK] Calculated returns: {len(returns)} values")
        print(f"  [OK] Annualized volatility: {vol:.2%}")
        print(f"  [OK] Sharpe ratio: {sharpe:.2f}")
        return True
        
    except Exception as e:
        print(f"  [ERROR] {e}")
        return False


def main():
    """Run all setup checks."""
    print("=" * 60)
    print("Stock Data Analysis - Setup Check")
    print("=" * 60)
    
    # Add src to path
    sys.path.insert(0, os.path.dirname(__file__))
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Yahoo Finance", test_yahoo_finance),
        ("Data Processing", test_data_processing),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n  [FAILED] {name} check failed with error: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Setup Check Summary")
    print("=" * 60)
    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    if all_passed:
        print("\nAll checks passed! You're ready to start.")
        print("\nNext steps:")
        print("  1. Run: python examples/basic_data_fetching.py")
        print("  2. Run: python examples/data_analysis.py")
        print("  3. Run: streamlit run app.py")
    else:
        print("\nSome checks failed. Please fix the issues above.")
    
    return all_passed


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

