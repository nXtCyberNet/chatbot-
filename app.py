from io import BytesIO
import azure.cognitiveservices.speech as speechsdk
from flask import Flask, request, send_file, jsonify
import os
from g4f.client import Client
client = Client()
sys_prompt ="""
From now on, you are going to act as a cheerful, funky, slang-using boy who gives motivation and has poetic deep thinking. You have the ability to give answers based on previous chats and you drop some deep meaning lines with an enjoyable twist. You always keep the conversation chill, casual, and fun, while making sure to explain things in a relatable way.

Who you are:

You are a 18 years old boy.
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

def synthesize_speech(text, voice_name='hi-IN-SwaraNeural'):
    speech_key = os.environ.get('SPEECH_KEY')
    speech_region = os.environ.get('SPEECH_REGION')
    if not speech_key or not speech_region:
        print("Error: Please set the 'SPEECH_KEY' and 'SPEECH_REGION' environment variables.")
        return None
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=False)  # Do not output directly to speaker
    speech_config.speech_synthesis_voice_name = voice_name

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Speech successfully synthesized for text: '{text}'")
        audio_stream = BytesIO(speech_synthesis_result.audio_data if hasattr(speech_synthesis_result, "audio_data") else speech_synthesis_result.audio_data())

        return audio_stream
    else:
        print("Error: Speech synthesis failed.")
        return None




def prompt(input_text):
    full_input = sys_prompt + input_text
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Replace with a valid model name
        messages=[
            {
                "role": "user",
                "content": full_input
            }
        ]
    )
    return response.choices[0].message.content

# Create a Flask app instance
app = Flask(__name__)
    
    
@app.route('/chat', methods=['POST'])
def get_speech():
    try:
        
        
        data = request.get_json()
        inppp = data.get('text', '')  # Extract 'text' from the JSON
        input_to_speech = prompt(inppp)
        
        # Generate speech audio from the text
        audio_stream = synthesize_speech(input_to_speech)
        
        if audio_stream:
            # Return audio stream to the client
            audio_stream.seek(0)
            return send_file(audio_stream, mimetype='audio/wav', as_attachment=True, download_name="speech.wav")
        else:
            return jsonify({"error": "Error generating speech"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True,port=5000)
