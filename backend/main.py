from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import httpx
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env

api_key = os.getenv("HIBP_API_KEY")

load_dotenv()
api_key = os.getenv("HIBP_API_KEY")
print("API Key loaded:", api_key)  # Add this line temporarily

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your actual frontend URL in production
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/check/email")
async def check_email(email: str):
    headers = {
        "hibp-api-key": api_key,
        "User-Agent": "osint-tool/1.0"
    }

    hibp_url = f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}"

    async with httpx.AsyncClient() as client:
        response = await client.get(hibp_url, headers=headers)

    if response.status_code == 200:
        return {
            "email": email,
            "breached": True,
            "breaches": response.json(),
        }
    elif response.status_code == 404:
        return {
            "email": email,
            "breached": False,
            "breaches": [],
        }
    else:
        return {
            "email": email,
            "error": f"Unexpected response from HIBP: {response.status_code} - {response.text}"
        }

