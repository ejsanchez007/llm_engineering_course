import os
import openai
from dotenv import load_dotenv

# Load env file
load_dotenv(override=True)

# Compatible endpoint URL for Google API
GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

# get the api key for google service
api_key = os.getenv('GOOGLE_API_KEY')

# create the openai client instance
gemini = openai.OpenAI(base_url=GEMINI_BASE_URL, api_key=api_key)

# create the messages list
messages = [
    {"role": "user", "content": "Tell me a fun fact"}
]

# make the request to the Google API
response = gemini.chat.completions.create(
    model="gemini-3.1-flash-lite",
    reasoning_effort="none",
    messages=messages
)

# Display the response message content
print(response.choices[0].message.content)