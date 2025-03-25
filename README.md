# Stock Market AI Agent 📈  

An AI-powered Flask API that fetches stock market data using `yfinance` and provides investment insights with Google Gemini AI via LangChain.  

## Features 🚀  
- Fetch stock price, company details, and market insights.  
- AI-powered stock analysis with Google Gemini.  
- Conversational chatbot for stock-related queries.  

## Installation 🛠  
1. **Clone the repo:**  

2. **Create a virtual environment & install dependencies:**
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
   
3. **Set up Google API Key:**
## Usage ▶
**Run the Flask app:**
python App.py

**API Endpoints:**

GET /stock_price?ticker=AAPL → Fetch stock price.

GET /stock_details?ticker=GOOGL → Get stock insights.

POST /chat → AI chatbot (send { "input": "Should I buy Tesla?" }).

