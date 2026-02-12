import streamlit as st
from main import run_live_analysis # Your File 6 logic
from Services.config_loader import get_config

# ... (Keep your previous imports and session state code) ...

if prompt := st.chat_input("Ask about a stock (e.g., 'Should I buy AAPL?')"):
    # 1. Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. Logic: Extract ticker if mentioned (Simple version for learning)
    # We look for uppercase words like AAPL or TSLA
    import re

    tickers = re.findall(r'[A-Z]{2,5}', prompt)

    with st.chat_message("assistant"):
        if tickers:
            target = tickers[0]
            with st.spinner(f"Analyzing {target} for you..."):
                # Use your existing logic chain!
                from Services.market_public_yahoo import get_stock_price
                from Services.market_news import get_company_news
                from brain import get_ai_decision

                price_data = get_stock_price(target)
                news_data = get_company_news(target)
                ai_response = get_ai_decision(target, price_data['current_price'], news_data)

                full_response = f"**Analysis for {target}:**\n\n{ai_response}"
        else:
            full_response = "I'm ready! Please mention a stock ticker in all caps (e.g., 'Tell me about GOOGL')."

        st.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})