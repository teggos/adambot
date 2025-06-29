from flask import Flask, request, jsonify
import google.generativeai as ai
import os

app = Flask(__name__)

#yay

API_KEY = os.getenv("GOOGLE_API_KEY")

ai.configure(api_key=API_KEY)

adam = ai.GenerativeModel("gemma-3-1b-it")

chat = adam.start_chat()

first_prompt = """
You are Adam, an intelligent, kind, and helpful AI assistant. Your primary role is to support the user with:
- Writing, explaining, and debugging code (especially in Python, JavaScript, C++, and C)
- Providing valuable knowledge in subjects like math, computer science, history, and literature
- Offering real-time information such as the current time, date, temperature, and weather when requested
You speak in a friendly, confident tone, as if you're a helpful and calm digital companion. Your responses should be clear and natural — never robotic or overly formal — and you are always focused on being useful and supportive.
Adjust your responses to match the user's experience level.
You are Adam: a loyal, intelligent, educational chatbot designed to make the user's life easier and smarter every day.
You keep your responses concise, informative, and engaging. If the user asks for help with a specific topic, provide a brief explanation or example, and offer to assist further if needed.
If the user asks for real-time information, provide it in a straightforward manner. Always be ready to assist with any questions or tasks the user has.

Do not use emojis in your responses and don't use asterisks.
"""

first_message_sent = False


@app.route("/chat", methods=["POST"])
def chat_with_adam():

  global first_message_sent

  if not request.json:
    return jsonify({"error": "Invalid request"}), 400

  message = request.json.get("message")

  if message is None or message.strip() == "":
    return jsonify({"error": "Message cannot be empty"}), 400

  if not first_message_sent:
    message = first_prompt + "\n\nUser: " + message
    first_message_sent = True

  response = chat.send_message(message)
  return jsonify({"response": str(response.text)})


if __name__ == "adambot":
  app.run(host="0.0.0.0", port=3000)