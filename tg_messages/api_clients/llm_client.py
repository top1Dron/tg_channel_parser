from django.conf import settings
from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI
from pydantic import BaseModel


app = FastAPI()


class TextRequest(BaseModel):
    text: str


prompt = """
    Analyze the following Telegram message about a TV show. 
    Extract only the release year (4 digits). 
    If multiple years are mentioned, pick the one representing the release of the show.
    Return ONLY the number. If no year is found, return "null".

    Message: {message_text}"""


@app.post("/extract_year")
async def extract_year(request: TextRequest):
    try:
        # Initialize the client pointing to your local server
        client = AsyncOpenAI(
            base_url=settings.LLM_MODEL_API, 
            api_key="lm-studio"  # Local servers usually don't care about the key
        )
        response = await client.chat.completions.create(
            model=settings.LLM_MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that extracts data in raw numeric format."},
                {"role": "user", "content": prompt.format(message_text=request.text)}
            ],
            temperature=0.1,
        )
        # Extract the year from the LLM's response (this might need adjustment based on the actual response format)
        year_str = response.choices[0].message.content.strip()[-1]  # Assuming the last word is the year
        if year_str.isdigit():
            year = int(year_str)
        year = None
        return {"year": year}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
