from flask import Flask, request, jsonify
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

client=OpenAI()

load_dotenv()

app=Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route('/')
def home():
    return "kid story stelling generator API is running!"

@app.route('/generate_story', methods=['POST'])
def generate_story():
    data =request.get_json()

    hero=data.get('hero')
    world=data.get('world')
    feeling=data.get('feeling')
    if not hero or not world or not feeling:
        return jsonify({'error: wrong details!'}), 400
    
    prompt= f""" Create stories for the kids with age above 3 to 9 y/o
    Hero: {hero}
    World:{world}
    Feeling:{feeling}
    A safe place for kids to enjoy. Avoid Scary or negative content.
    """

    try:
        response= client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"system", "content":"You are a friendly kid story telling application"}, 
                      {"role": "user","content": prompt }],

            temperature=0.7,
            max_tokens=300
        )
        story = response.choices[0].message.content
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__=='__main__':
    app.run(debug=True)
