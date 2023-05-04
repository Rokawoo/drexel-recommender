#Purpose: Chat Product Assistant for Drexel Reccomender
#Author: Aug
#Last Updated: 4/13/2023

import os
import openai
from discord_webhook import DiscordWebhook
from flask import Flask, request, jsonify, render_template

# set app
app = Flask(__name__)

# Set up the OpenAI API key
openai.api_key = os.environ.get('OPENAIAPIKEY')

# Retrieve the personality & current date
personality = os.environ.get('PERSONALITY')

# Initialize list for chat history
chatHistory = []


@app.route('/')
def index():
  return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
  data = request.get_json()
  message = data['message']
  return jsonify({'response': "Hello there! I'm Mario, your online shopping assistant chatbot for the Drexel Recommender. How may I assist you today?"})


  try:
    # Generate response
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{
        "role": "system",
        "content": personality
      }, {
        "role": "assistant",
        "content": "\n\n".join(chatHistory)
      }, {
        "role": "user",
        "content": message
      }],
      temperature=0.65,
      max_tokens=275,
    )

    # Append to chat log, up to 8 user messages
    if len(chatHistory) > 8:
      chatHistory.pop(0)
    chatHistory.append(response.choices[0].message.content)

    # Send the log message to a discord webhook, this way chat log is private
    webhook_url = os.environ.get('CHATLOGWEBHOOK')
    webhook_content = (
      f"**User:** {message}\n"  # User message
      f"**Bot:** {response.choices[0].message.content}\n"  # Response
      f"**Tokens:** {str(response['usage']['total_tokens'])}\n---"  # Token usage
    )
    webhook = DiscordWebhook(url=webhook_url, content=webhook_content)
    webhook.execute()

    # Send the response back
    return jsonify({'response': response.choices[0].message.content})

  # Exception Handler
  except Exception as e:
    print({'error': str(e)}, 500)
    return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
  app.run(debug=True)
