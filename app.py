from flask import Flask, request, jsonify
import os

app=Flask(__name__)

@app.route('/')
def home():
    return "kid story stelling generator API is running!"

if __name__=='__main__':
    app.run(debug=True)
