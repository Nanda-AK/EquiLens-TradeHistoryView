import os
from crewai import Crew, Task
from yfinance import Ticker
from langchain import OpenAI
from langchain.agents import create_pandas_dataframe_agent

# Task for CrewAI to fetch the live price of a given symbol
def fetch_current_price(context):
    symbol = context.get("symbol")
    try:
        ticker = Ticker(symbol)
        price = ticker.info.get("regularMarketPrice")
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
        # run a single-task Crew flow
        result = crew.run({"symbol": symbol})
        prices[symbol] = result.get("current_price")
    summary_df["Current Price"] = summary_df["Stock Name"].map(prices)
    return summary_df

# Create a LangChain React-style agent for chatting with the DataFrame
def create_summary_agent(summary_df):
    # Assumes OPENAI_API_KEY is set in env (e.g. via Streamlit secrets)
    llm = OpenAI(temperature=0)
    agent = create_pandas_dataframe_agent(
        llm,
        summary_df,
        agent_type="react"
    )
    return agent
