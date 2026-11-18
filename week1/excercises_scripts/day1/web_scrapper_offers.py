import os
from pyexpat.errors import messages
from dotenv import load_dotenv
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

    response = openai.chat.completions.create(model="gpt-6-luna", reasoning_effort="none", messages=messages)
    
    return response.choices[0].message.content

load_dotenv(override=True)
api_key = os.getenv('OPENAI_API_KEY')

openai = OpenAI()

url = "https://www.soriana.com/ofertas/"
topic = "screens"
target_discount = 30

print(find_related_offers(url, topic, target_discount))
