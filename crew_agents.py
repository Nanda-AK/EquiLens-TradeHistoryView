import pysqlite3, sys
# Monkey-patch stdlib sqlite3 to use pysqlite3-binary (SQLite>=3.35)
sys.modules['sqlite3'] = pysqlite3

import os
from crewai import Crew, Task
from yfinance import Ticker
# Import OpenAI LLM directly to avoid langchain_community fallback
from langchain.llms.openai import OpenAI
from langchain.agents import create_pandas_dataframe_agent

# Task to fetch the live price of a given symbol
def fetch_current_price(context):
    symbol = context.get("symbol")
    try:
        ticker = Ticker(symbol)
        price = ticker.info.get("regularMarketPrice") or ticker.info.get("currentPrice")
    except Exception:
        price = None
    context["current_price"] = price
    return context

# Enrich a summary DataFrame by adding a "Current Price" column via CrewAI
def enrich_current_prices(summary_df):
    crew = Crew()
    crew.add_task(Task(name="fetch_price", run=fetch_current_price))
    prices = {}
    for symbol in summary_df["Stock Name"].unique():
        result = crew.run({"symbol": symbol})
        prices[symbol] = result.get("current_price")
    summary_df["Current Price"] = summary_df["Stock Name"].map(prices)
    return summary_df

# Create a LangChain React-style agent for chatting with the DataFrame
def create_summary_agent(summary_df):
    # Ensure API key is set in environment before calling this
    llm = OpenAI(temperature=0)
    agent = create_pandas_dataframe_agent(
        llm,
        summary_df,
        agent_type="react"
    )
    return agent
