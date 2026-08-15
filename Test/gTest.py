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
class GeneralQueryRequest(BaseModel):
    user_prompt: str


@router.post("/query")
def get_general_response(request: GeneralQueryRequest):
    try:
        custom_rules = """
        1. Answer ONLY if questions related to the Stock Market are asked.
        2. If the user prompt is not about stocks and the stock market and is unrelated to the stock market, inform the user politely that they must ask questions related to stocks and the stock market only.
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