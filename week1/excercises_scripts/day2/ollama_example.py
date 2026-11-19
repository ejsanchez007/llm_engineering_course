import openai

def display_menu():
    print("Select a model:")
    counter = 1
    for model in AVAILABLE_MODELS:
        print(f"{counter}. {model}")
        counter += 1
    choice = int(input("Enter the number of your choice: "))
    return AVAILABLE_MODELS[choice - 1]

AVAILABLE_MODELS = ("llama3.2", "deepseek-r1:1.5b")

#Client settings
OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"
ollama_api_key = "ollama" # can be anything as it's local and free

# Create the OpenAI client instance for Ollama
ollama = openai.OpenAI(base_url=OLLAMA_BASE_URL, api_key=ollama_api_key)

# Create the messages list
messages = [
    {"role": "user", "content": "Tell me a fun fact"}
]

# Get the selected model from the user and make the request to the Ollama API
selected_model = display_menu()
response = ollama.chat.completions.create(
    model=selected_model,
    reasoning_effort="none",
    messages=messages
)

# Display the response message content
print(response.choices[0].message.content)