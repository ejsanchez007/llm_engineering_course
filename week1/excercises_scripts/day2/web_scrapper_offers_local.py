import os
from openai import OpenAI
from scraper import fetch_rendered_contents

def find_related_offers(url, topic, target_discount = 10):
    site_contents = fetch_rendered_contents(url, max_chars=10000)

    system_prompt = """
    You're a web page contents analyzer that finds any requested information in the contents of a website, 
    and provides it in a human readable format displayed in the terminal.
    """

    user_prompt = f"""
    Find all the offers greater than {target_discount}% discount related to {topic} in the following 
    website contents, include the discount percentage:
    {site_contents}
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    response = ollama.chat.completions.create(model=MODEL, reasoning_effort="none", messages=messages)
    
    return response.choices[0].message.content

API_KEY = "ollama"
BASE_URL = "http://127.0.0.1:11434/v1"
MODEL = "llama3.2"

ollama = OpenAI(base_url=BASE_URL, api_key=API_KEY)

url = "https://www.soriana.com/ofertas/"
topic = "screens"
target_discount = 30

print(find_related_offers(url, topic, target_discount))
