import pysqlite3, sys
# Monkey-patch stdlib sqlite3 to use pysqlite3-binary (SQLite>=3.35)
sys.modules['sqlite3'] = pysqlite3

import os
from crewai import Crew, Task
from yfinance import Ticker
from langchain.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Task to fetch the live price of a given symbol
def fetch_current_price(context):
    symbol = context.get("symbol")
    try:
        ticker = Ticker(symbol)
        # Use regularMarketPrice or fallback to currentPrice
        price = ticker.info.get("regularMarketPrice") or ticker.info.get("currentPrice")
    except Exception:
        price = None
    context["current_price"] = price
    return context

# Enrich a summary DataFrame by adding a "Current Price" column via CrewAI
def enrich_current_prices(summary_df):
    # Define the Task with description and expected_output
    fetch_task = Task(
        name="fetch_price",
        description="Fetch current market price for a given stock symbol",
        expected_output="current_price",
        run=fetch_current_price
    )
    # Instantiate Crew with tasks list
    crew = Crew(tasks=[fetch_task])
    prices = {}
    for symbol in summary_df["Stock Name"].unique():
        # Run the single-task crew flow
        result = crew.run({"symbol": symbol})
        prices[symbol] = result.get("current_price")
    summary_df["Current Price"] = summary_df["Stock Name"].map(prices)
    return summary_df

# Create a LangChain React-style agent for chatting with the DataFrame
def create_summary_agent(summary_df):
    # Ensure OPENAI_API_KEY is set in environment
    llm = ChatOpenAI(temperature=0)
    agent = create_pandas_dataframe_agent(
        llm,
        summary_df,
        agent_type="react"
    )
    return agent
