def should_i_alert_user(market_data, ai_decision):
    """
    Determines if a notification should actually be sent to your iPhone.
    Uses basic threshold logic + AI sentiment.
    """

    # 1. Extract the movement percentage
    current = market_data['current_price']
    avg = market_data['5_day_avg']
    price_change_pct = ((current - avg) / avg) * 100

    # 2. Logic Gates
    is_big_move = abs(price_change_pct) > 2.0  # More than 2% move
    is_urgent_ai = "SELL" in ai_decision.upper()

    # 3. Decision
    if is_urgent_ai and is_big_move:
        return True, f"🚨 URGENT: {price_change_pct:.2f}% drop & AI says SELL."

    if is_urgent_ai:
        return True, "⚠️ CAUTION: AI recommends SELL based on news."

    if price_change_pct > 5.0:
        return True, f"📈 MOON ALERT: {market_data['symbol']} is up {price_change_pct:.2f}%!"

    return False, "No urgent action needed."


# Test block
if __name__ == "__main__":
    mock_market = {"symbol": "NVDA", "current_price": 100, "5_day_avg": 110}  # 10% drop
    mock_ai = "The news is terrible, you should SELL immediately."

    should_alert, reason = should_i_alert_user(mock_market, mock_ai)
    print(f"Should Alert: {should_alert}")
    print(f"Reason: {reason}")