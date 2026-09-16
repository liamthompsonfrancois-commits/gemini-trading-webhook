import os
from fastapi import FastAPI, Request
import uvicorn
from google import genai

app = FastAPI()

# Initialize the Gemini client automatically using your environment variable
client = genai.Client()

@app.get("/")
def home():
    return {"status": "Server is live and running!"}

@app.post("/webhook")
async def tradingview_webhook(request: Request):
    try:
        data = await request.json()
        ticker = data.get("ticker", "Unknown")
        price = data.get("close", 0)
        rsi = data.get("rsi", 50)
        ema200 = data.get("ema200", 0)

        prompt = f"""
        Act as an expert technical analyst trading system. Analyze this data point:
        Asset: {ticker}
        Current Price: ${price}
        14-Period RSI: {rsi}
        200-period EMA: {ema200}

        Reply in exactly this layout:
        SIGNAL: [BUY, SELL, or HOLD]
        REASON: [One short sentence explaining your logic]
        """

        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )

        print(f"\n--- New Signal Received for {ticker} ---")
        print(response.text.strip())
        
        return {"status": "success", "signal_processed": True}

    except Exception as e:
        print(f"Error handling webhook: {e}")
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
