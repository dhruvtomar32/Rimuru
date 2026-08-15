import os
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel

# Initialize Router
router = APIRouter()

# Load environment variables
load_dotenv()

# Retrieve API key
GEMINI_API_KEY = os.getenv("GCP_API_KEY")

# Initialize Google GenAI Client
client = genai.Client(api_key=GEMINI_API_KEY)


# Request schema
class StockRequest(BaseModel):
    user_prompt: str
    stock_name: str


@router.post("/stock-query")
def get_stock_response(request: StockRequest):
    try:
        custom_rules = f"""
        1. Answer ONLY if questions related to {request.stock_name} are asked.
        2. If the prompt does not pertain to {request.stock_name} and is unrelated to {request.stock_name}, inform the user politely that they must ask questions related to {request.stock_name} only.
        """

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=request.user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=custom_rules,
            ),
        )

        return {"status": "success", "response": response.text}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))