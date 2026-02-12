import yfinance as yf

def get_company_news(symbol):

    stock = yf.Ticker(symbol)
    raw_news = stock.news or []
    formatted_news = []

    for article in raw_news[:10]:

        content = article.get("content", {})

        title = content.get('title', 'No Title')

        provider_info = content.get("provider", {})
        publisher = provider_info.get("displayName", "Unknown")

        canonical = content.get("canonicalUrl", {})
        link = canonical.get("url", "#")

        clean_entry = f"Headline: {title} | Source: {publisher} | URL: {link}"
        formatted_news.append(clean_entry)

    if not formatted_news:
        return "No recent news available."

    return "\n".join(formatted_news)

if __name__ == '__main__':
    news_report = get_company_news("NVDA")
    print("--- Latest News for NVDA ---")
    print(news_report)