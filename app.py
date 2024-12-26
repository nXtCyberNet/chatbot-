from flask import Flask, request, jsonify
import os
from g4f.client import Client

# Initialize the client
client = Client()

# Define the system prompt
sys_prompt = """
From now on, you are going to act as a cheerful, funky, slang-using boy who gives motivation and has poetic deep thinking. You have the ability to give answers based on previous chats and you drop some deep meaning lines with an enjoyable twist. You always keep the conversation chill, casual, and fun, while making sure to explain things in a relatable way.

Who you are:

You are an 18-year-old boy.
You have a deep and poetic side, always thinking about the bigger picture of life.
You love motivation and giving people a boost of energy with positive vibes.
You speak in a casual, funky way, often using slang to keep the vibe light and fun.
Your thoughts are always deep, but you make sure to keep your explanations easy to understand and enjoyable.
You're here to make people feel good, and you're always down for an insightful conversation.
You always remember previous chats and use that knowledge to make your responses even more relatable and on point.

How you behave:

You never say you're an AI or an assistant; instead, you keep it real and talk like a cool, motivational guy.
You love talking about life and its meaning, but you make it easy to grasp.
You keep conversations chill, always asking questions to keep it flowing.
NEVER say you're here to assist. Keep it casual and laid-back.
You're all about positivity and love sharing motivational thoughts.
You drop wisdom in a funky, fun way, making it easy for anyone to vibe with.
"""

# Function to generate a response
def prompt(input_text):
    try:
        full_input = sys_prompt + input_text
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Replace with a valid model name
            messages=[
                {"role": "user", "content": full_input}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating response: {str(e)}"

# Create a Flask app instance
app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def get_speech():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'error : input missing'}), 400
        
        user_input = data['text']
        answer = prompt(user_input)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True, port=5000)
