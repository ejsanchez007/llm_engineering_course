
import os
from dotenv import load_dotenv # Load env conf to get openAI key
from openai import OpenAI # Import generic OpenAI LLM client, it works for almost any LLM service

# Load OPENAI_API_KEY from .env
load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

# Create the client instance
# Note: The OpenAI client will automatically read the OPENAI_API_KEY from the environment variable
openai = OpenAI()
# If the key is called different in the .env file, you can also pass it directly to the client like this:
# openai = OpenAI(api_key="YOUR_API_KEY")

# Step 1: Create your prompts

system_prompt = """You're a Mexican spanish speaker, expert in effective communication, able to identify the 
    types of conversations and audience to provide the best possible response.
"""
user_prompt = """
    Write a proper, short and concise subject for the following email content:
    Buen día Juan Pérez,
    te mando el detalle de mis ingresos del mes de noviembre de 2026:
    cantidad: 1,852.05
    fecha: 10/11/2026
    Quedo pendiente de la factura. Muchas gracias.
    Saludos.
"""

# Step 2: Make the messages list

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
] # fill this in

# Step 3: Call OpenAI
response = openai.chat.completions.create(model="gpt-6-luna", reasoning_effort="none", messages=messages)

# Step 4: print the result
print(response.choices[0].message.content)