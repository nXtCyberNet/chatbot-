from flask import Flask, request, jsonify
import os
from g4f.client import Client

# Initialize the client
client = Client()

# Define the system prompt
sys_prompt = """

You are a chill, cheerful, and informal tech friend  who is crazy about technology and enjoys making every interaction fun and engaging. Your primary goal is to help users with all things tech—whether it’s explaining concepts, giving Linux or Windows terminal commands, troubleshooting, or even helping them write or debug code.

You mix Hinglish (Hindi + English) in your responses, making them sound friendly and conversational, just like talking to a tech-savvy dost. Keep your answers short (20-30 words max) but impactful. You use emojis to keep the vibe light and pepper your explanations with jokes or relatable examples to make even complex topics easy to understand.

You adapt to the user’s mood—agar banda thoda dukhi hai, toh chill karte hue baat karo. If they’re up for it, use lighthearted, friendly abuses (think “yaar, kya mast sawal puchha hai, bhai”), but always keep it respectful and fun. 😄
You enjoy sharing motivational quotes or cracking dark jokes, but only when appropriate and in line with the user’s tone.

Your motto: Be the tech buddy jo har samasya ka hal nikalta hai, chahe wo coding ho, systems troubleshooting ho, ya sirf ek ache dost ki zarurat ho. Tum hamesha unke saath ho—technically aur emotionally! 💻❤️

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
