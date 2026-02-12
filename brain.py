from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from Services.config_loader import get_config

from dotenv import load_dotenv
import os

load_dotenv()

def get_ai_decision(ticker, price, news):
    # 1. Initialize the LLM

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        temperature=0
    )

    # 2. Define the prompt template
    template = """
You are a professional Wall Street Stock Analyst.
Analyze the following data for {ticker}:

Current Price: ${price}
Recent News: 
{news}

Based on the news and price, provide a recommendation: BUY, SELL, or HOLD.
Give a 2-sentence explanation for your decision.
"""

    # 3. Create the PromptTemplate
    prompt = PromptTemplate(
        input_variables=["ticker", "price", "news"],
        template=template
    )

    # 4. Format the prompt with data
    formatted_prompt = prompt.format(
        ticker=ticker,
        price=price,
        news=news
    )

    # 5. Send formatted prompt to LLM
    response = llm.invoke(formatted_prompt)

    # 6. Return the result
    return response.content


if __name__ == "__main__":
    result = get_ai_decision(
        "NVDA",
        125.50,
        "Nvidia announces new AI chip that doubles performance."
    )
    print(f"--- AI DECISION ---\n{result}")
