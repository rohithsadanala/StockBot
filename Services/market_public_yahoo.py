import yfinance as yf
import pandas as pd

def get_stock_price(ticker_symbol: str):

    stock = yf.Ticker(ticker_symbol)
    current_price = stock.fast_info["lastPrice"]
    history = stock.history(period="1d")
    average_price = history["Close"].mean()

    return {
        'ticker_symbol': ticker_symbol,
        'current_price': round(current_price, 2),
        'average_price': round(average_price, 2),
    }

if __name__ == '__main__':
    data = get_stock_price('NVDA')
    print(f"Data for {data['ticker_symbol']}: ${data['current_price']}")