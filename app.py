from flask import Flask, request, jsonify
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client=OpenAI()

app=Flask(__name__)
openai.api_key = os.getenv('OPENAI_API_KEY')

Blocked_Keywords =["kill","abuse","blood","die","gun","knife","blood","violence"]

story_log =[]

def is_story_safe(text):
    for word in Blocked_Keywords:
        if word.lower() in text.lower():
            return False 
        return True

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
        

        if not is_story_safe(story):
            return jsonify({"error": "Story not safe for children."}), 400
        
        story_entry = {
            "id": len(story_log) + 1,
            "hero": hero,
            "world": world,
            "feeling": feeling,
            "story": story,
            "approved": False
        }
        story_log.append(story_entry)

        return jsonify({"story": story})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/parent/review_stories', methods=['GET'])
def review_stories():
    return jsonify({"stories": story_log})


if __name__=='__main__':
    app.run(debug=True)
