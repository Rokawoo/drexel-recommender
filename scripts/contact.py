#Purpose: Send Webinput to Discord Webhook
#Author: Aug
#Last Updated: 4/30/2023

from discord_webhook import DiscordWebhook
from flask import Flask, request, jsonify, render_template

# set app
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('contact.html')

@app.route('/contact', methods=['POST'])
def sendContact():
  email = request.form['email']
  message = request.form['message']

  try:
    # Send the log message to a discord webhook, this way chat log is private
    webhook_url = 'https://discord.com/api/webhooks/1102401542742605934/Q5EcnS1V2dq3OIjn8zv9-kLcsXjDv-_JVymJMSlgaoWI6bAflM3XOBcBnVNrpB3U5HcK'
    webhook_content = (f"**Email:** {email}\n\n**Message:** {message}\n---")  # User message
    webhook = DiscordWebhook(url=webhook_url, content=webhook_content)
    webhook.execute()

    # Send the confirmation response back
    return jsonify({'response': 'Your message has been sent.'})

  # Exception Handler
  except Exception as e:
    print({'error': str(e)}, 500)
    return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
  app.run(debug=True)
