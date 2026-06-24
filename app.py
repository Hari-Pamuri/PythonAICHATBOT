from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

print("AI Chatbot Started! Type 'exit' to quit.")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_input
        )

        print("AI:", response.text)

    except Exception as e:
        print(type(e))
        print("ERROR:", str(e))