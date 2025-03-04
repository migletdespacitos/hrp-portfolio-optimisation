import yfinance as yf
import pandas as pd
import numpy as np
from pypfopt import HRPOpt, expected_returns, risk_models
from datetime import datetime

# Step 1: Fetch Historical Stock Data and Handle Missing Data
def get_stock_data(tickers, start_date, end_date):
    tickers = [ticker.strip().upper() for ticker in tickers]
    try:
        data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']
        if data.empty:
            print("No data fetched. Please check the tickers and date range.")
            return pd.DataFrame()
        data = data.ffill().dropna()  # Forward-fill missing data
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

# Step 2: Build HRP Portfolio
def build_hrp_portfolio(data):
    try:
        cov_matrix = risk_models.sample_cov(data)
        hrp = HRPOpt(cov_matrix)
        weights = hrp.optimize()
        return weights
    except Exception as e:
        print(f"Error building HRP portfolio: {e}")
        return {}

# Step 3: Calculate Expected Portfolio Return and Volatility
def calculate_portfolio_metrics(data, weights):
    try:
        mu = expected_returns.mean_historical_return(data)
        weights_series = pd.Series(weights)
        expected_return = mu.dot(weights_series)
        cov_matrix = risk_models.sample_cov(data)
        portfolio_volatility = np.sqrt(weights_series.T @ cov_matrix @ weights_series)
        return expected_return, portfolio_volatility
    except Exception as e:
        print(f"Error calculating portfolio metrics: {e}")
        return 0.0, 0.0

# Step 4: Fetch Latest Prices for Asset Allocation
def fetch_latest_prices(tickers):
    try:
        latest_prices = yf.download(tickers, period="1d", auto_adjust=True)['Close']

        # Ensure latest_prices is a Pandas Series (not DataFrame)
        if isinstance(latest_prices, pd.DataFrame):
            latest_prices = latest_prices.iloc[-1]  # Get the last row (latest prices)

        return latest_prices.astype(float)  # Ensure values are floats
    except Exception as e:
        print(f"Error fetching latest prices: {e}")
        return pd.Series(dtype=float)

# Step 5: Allocate Funds Based on Latest Prices
def allocate_capital(weights, initial_capital, latest_prices):
    allocation = {}
    remaining_cash = initial_capital

    for ticker, weight in weights.items():
        amount_to_invest = weight * initial_capital
        share_price = latest_prices.get(ticker, np.nan)

        if pd.isna(share_price) or share_price <= 0:
            print(f"Skipping {ticker} due to invalid price.")
            continue

        num_shares = amount_to_invest / share_price
        allocation[ticker] = num_shares
        remaining_cash -= amount_to_invest

    return allocation, remaining_cash

# Step 6: Run the HRP Portfolio Strategy
def run_hrp_portfolio():
    # User Inputs
    tickers_input = input("Enter stock tickers (comma separated, e.g., AAPL, MSFT, GOOGL): ")
    tickers = tickers_input.split(',')
    tickers = [ticker.strip().upper() for ticker in tickers if ticker.strip()]
    
    if not tickers:
        print("No valid tickers entered. Exiting.")
        return

    start_date = input("Enter start date (YYYY-MM-DD, e.g., 2020-01-01): ")
    end_date = input("Enter end date (YYYY-MM-DD, e.g., 2023-12-31): ")
    
    # Validate date formats
    try:
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Incorrect date format. Please use YYYY-MM-DD.")
        return

    initial_capital_input = input("Enter initial capital (e.g., 10000): ")
    try:
        initial_capital = float(initial_capital_input)
        if initial_capital <= 0:
            print("Initial capital must be a positive number.")
            return
    except ValueError:
        print("Invalid capital amount. Please enter a numeric value.")
        return

    # Step 1: Fetch Data
    data = get_stock_data(tickers, start_date, end_date)
    if data.empty:
        print("No data available for the provided tickers and date range.")
        return

    # Step 2: Build HRP Portfolio
    weights = build_hrp_portfolio(data)
    if not weights:
        print("Failed to build HRP portfolio.")
        return

    # Step 3: Calculate expected portfolio return and volatility
    expected_return, portfolio_volatility = calculate_portfolio_metrics(data, weights)

    # Step 4: Fetch the latest prices
    latest_prices = fetch_latest_prices(tickers)
    if latest_prices.empty:
        print("Failed to fetch latest prices. Cannot proceed with allocation.")
        return

    # Step 5: Capital allocation based on the latest prices
    allocation, remaining_cash = allocate_capital(weights, initial_capital, latest_prices)

    # Step 6: Display results
    print("\nOptimized Portfolio Weights:")
    for ticker, weight in weights.items():
        print(f"{ticker}: {weight * 100:.2f}%")

    print(f"\nExpected Annual Return: {expected_return * 100:.2f}%")
    print(f"Portfolio Volatility (Standard Deviation): {portfolio_volatility * 100:.2f}%")
    print(f"\nCapital Allocation based on Initial Capital (${initial_capital:,.2f}):")
    
    for ticker, shares in allocation.items():
        price = latest_prices.get(ticker, np.nan)

        if pd.isna(price):
            print(f"{ticker}: Unable to retrieve price.")
        else:
            print(f"{ticker}: {shares:.4f} shares @ ${float(price):.2f} each")

    print(f"\nRemaining Cash: ${remaining_cash:.2f}")

# Run the strategy with user inputs
if __name__ == "__main__":
    run_hrp_portfolio()
