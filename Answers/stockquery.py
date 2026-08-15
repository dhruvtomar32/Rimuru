from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from google.genai import types
import os
from dotenv import load_dotenv



app = FastAPI()

# Store API key in script as requested
# Load environment variables from .env file
load_dotenv()

# Retrieve your API key securely
GEMINI_API_KEY = os.getenv("GCP_API_KEY")

# Initialize Google GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)


# Request schema matching expected payload from FlutterFlow
class StockRequest(BaseModel):
    user_prompt: str
    stock_name: str


@app.post("/stock-query")
def get_stock_response(request: StockRequest):
    try:
        # Define dynamic system instructions based on incoming stock name
        custom_rules = f"""
        1. Answer ONLY if questions related to {request.stock_name} are asked.
        2. If the prompt is Doesn't consist {request.stock_name} and is unrelated to {request.stock_name}, inform the user politely that they must ask questions related to {request.stock_name} only.
        """

        # Corrected Gemini API call
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=request.user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=custom_rules,
                # Optional: Enable Google Search Grounding for real-time stock info
                # tools=[{"google_search": {}}]
            ),
        )

        return {"status": "success", "response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))