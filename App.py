import os
from flask import Flask, request, jsonify
import yfinance as yf
from langchain.memory import ConversationBufferMemory
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_google_genai import ChatGoogleGenerativeAI

os.environ["GOOGLE_API_KEY"] = "MYKEY" 
model_name = "gemini-1.5-flash"

llm = ChatGoogleGenerativeAI(model=model_name, temperature=0, google_api_key=os.environ["GOOGLE_API_KEY"])

app = Flask(__name__)

def fetch_stock_price(ticker: str):
    """Get basic stock information for a given ticker"""
    stock = yf.Ticker(ticker)
    info = stock.info

    if "currentPrice" not in info:
        return {"error": "Invalid ticker symbol or data unavailable"}

    return {
        "currentPrice": info.get("currentPrice"),
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "website": info.get("website"),
        "longBusinessSummary": info.get("longBusinessSummary")
    }

#  Function to analyze stock and provide Buy/Sell/Hold recommendation
def fetch_stock_details(ticker: str):
    """Fetch stock details and provide investment recommendation"""
    stock = yf.Ticker(ticker)
    info = stock.info

    if "currentPrice" not in info:
        return {"error": "Invalid ticker symbol or data unavailable"}

    price = info.get("currentPrice")
    long_name = info.get("longName", "Unknown Company")
    summary = info.get("longBusinessSummary", "No summary available.")

    if price > 200:
        recommendation = " **Sell** - The stock is overvalued. Consider booking profits."
    elif 100 <= price <= 200:
        recommendation = " **Hold** - The stock is stable. Monitor for trends."
    else:
        recommendation = " **Buy** - The stock is undervalued. Consider investing."

    return {
        "analysis": f" **{long_name} ({ticker})**\n🔹 **Latest Price:** {price} USD\n **Trend Analysis:** {recommendation}\n\n **Company Summary:** {summary}"
    }

@app.route("/")
def home():
    return " Stock Market AI Agent is Running!"

@app.route("/stock_price", methods=["GET"])
def get_stock_price():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    return jsonify(fetch_stock_price(ticker.upper()))

@app.route("/stock_details", methods=["GET"])
def get_stock_details():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Ticker symbol is required"}), 400

    return jsonify(fetch_stock_details(ticker.upper()))

memory = ConversationBufferMemory()

tools = [
    Tool(name="getPrice", func=fetch_stock_price, description="Fetches stock price"),
    Tool(name="getDetails", func=fetch_stock_details, description="Fetches stock details & analysis")
]

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("input", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = agent.run(user_input)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
