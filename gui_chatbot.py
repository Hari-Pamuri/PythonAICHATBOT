import customtkinter as ctk
from google import genai
from dotenv import load_dotenv
import os
import threading

# ---------- API ----------
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ---------- UI ----------
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1000x650")
app.title("AI Chatbot")

chat_history = []

# ---------- FUNCTIONS ----------
def new_chat():
    global chat_history
    chat_history = []
    chat_box.delete("1.0", "end")


def clear_chat():
    chat_box.delete("1.0", "end")


def get_ai_response():
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=chat_history
    )
    return response.text


def send_message(event=None):
    message = user_entry.get()

    if message.strip() == "":
        return

    chat_box.insert("end", f"\nYou: {message}\n")
    chat_box.see("end")

    user_entry.delete(0, "end")

    chat_history.append(
        {
            "role": "user",
            "parts": [message]
        }
    )

    chat_box.insert("end", "AI: Typing...\n")
    chat_box.see("end")

    def run_ai():
        reply = get_ai_response()

        chat_history.append(
            {
                "role": "model",
                "parts": [reply]
            }
        )

        chat_box.insert("end", f"AI: {reply}\n\n")
        chat_box.see("end")

    threading.Thread(target=run_ai, daemon=True).start()


# ---------- SIDEBAR ----------
sidebar = ctk.CTkFrame(app, width=180)
sidebar.pack(side="left", fill="y", padx=5, pady=5)

title_label = ctk.CTkLabel(
    sidebar,
    text="AI Chatbot",
    font=("Arial", 22, "bold")
)
title_label.pack(pady=20)

new_chat_btn = ctk.CTkButton(
    sidebar,
    text="New Chat",
    command=new_chat
)
new_chat_btn.pack(pady=10)

clear_btn = ctk.CTkButton(
    sidebar,
    text="Clear Chat",
    command=clear_chat
)
clear_btn.pack(pady=10)

# ---------- MAIN ----------
main_frame = ctk.CTkFrame(app)
main_frame.pack(side="right", fill="both", expand=True)

chat_box = ctk.CTkTextbox(main_frame)
chat_box.pack(fill="both", expand=True, padx=10, pady=10)

input_frame = ctk.CTkFrame(main_frame)
input_frame.pack(fill="x", padx=10, pady=10)

user_entry = ctk.CTkEntry(
    input_frame,
    placeholder_text="Type your message...",
    width=700
)
user_entry.pack(side="left", padx=10)

send_btn = ctk.CTkButton(
    input_frame,
    text="Send",
    command=send_message
)
send_btn.pack(side="left")

# Enter key
user_entry.bind("<Return>", send_message)

app.mainloop()