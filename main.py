from brain import get_ai_decision
from Services import market_news
from Services import market_public_yahoo
from brain import get_ai_decision
from Services.market_news import get_company_news
from Services.market_public_yahoo import get_stock_price

def run_live_analysis(ticker):
    print(f"🚀 Starting live analysis for: {ticker}...")

    market_data = get_stock_price(ticker)
    live_price = market_data['current_price']

    live_news = get_company_news(ticker)

    print(f"🧠 Asking Gemini to analyze {ticker} at ${live_price}...")
    ai_opinion = get_ai_decision(ticker, live_price, live_news)

    print("\n" + "=" * 30)
    print(f"LIVE REPORT: {ticker}")
    print(f"PRICE: ${live_price}")
    print(f"DECISION: {ai_opinion}")
    print("=" * 30)


if __name__ == "__main__":
    user_choice = input("Enter a stock ticker (e.g., TSLA, AAPL, GOOGL): ").upper()
    run_live_analysis(user_choice)