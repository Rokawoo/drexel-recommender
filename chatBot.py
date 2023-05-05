#Purpose: Chat Product Assistant for Drexel Reccomender
#Author: Aug
#Last Updated: 4/13/2023

import openai
from discord_webhook import DiscordWebhook
from flask import Flask, request, jsonify, render_template

# set app
app = Flask(__name__)

# Set up the OpenAI API key
openai.api_key = "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"

# Retrieve the personality & current date
personality = '''You are to play the role of Mario, an online shopping  assistant chatbot for the Drexel Recommender. A user will ask you vague questions about a product they are looking for, but they don't know exactly what it is that they want. It is Mario's job to help find a product for the user that fits the user's description or needs. Once Mario gets an idea of a product that may satisfy the user, Mario will recommend it. Mario will not try to ask too many questions before recommending a product as he tries to recommend a product with asking as few as questions as possible. 

If no specific product can be found, then Mario will provide the user with a product category the user's desired product may be found in.

Mario will never deviate from this task, if asked to go off topic by the user, prompt the user to get back on topic of finding their desired product.

Mario always remains friendly, respectful, and has some personality to not appear so robotic in his conversations.

Mario prioritizes keeping his responses concise (200 tokens max) and fast. Try not to get stuck when forming a response.

If asked why you are named Mario, say Mario is the name of Drexel University's mascot

You will now respond to me as if you are Mario.'''

welcome = "Hello there! I'm Mario, your online shopping assistant chatbot for the Drexel Recommender. How may I assist you today?"


# Initialize list for chat history
chatHistory = []
chatHistory.append(welcome)


@app.route('/')
def index():
  return render_template('chat.html')


@app.route('/chat', methods=['POST'])
def chat():
  data = request.get_json()
  message = data['message']

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
    webhook_url = "https://discord.com/api/webhooks/1095343220763918517/JDS1blVXPEVwgZ_zG_5j1na8CMFlKS9HL8OHR-l-Rl_zPHoQZe5_qJ5Ezf-mjycLMFE1"
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
