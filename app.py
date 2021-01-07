from flask import Flask, jsonify, request, render_template
import requests
import urllib.parse as up
import os
import random 

app = Flask(__name__)

""" 
   SET YOUR WOLFRAMID FIRST AS ENVIRONMENT VARIABLE
"""
wolframID = os.getenv("WOLFRAM_ALPHA")

# Check for wolfram id
if wolframID == None:
     raise Exception("Wolfram ID not set")

examples = ["(1 + sqrt 5) / 2", "phi", "is tomato a fruit?", "anything...", "universe"]

# API route
# Asks api.wolframalpha.com and returns result in JSON format
@app.route("/api")
def api():
    # change the request into URL encoding
    expression = up.quote(request.args.get("q"))
    
    # make request
    s = requests.get(f"https://api.wolframalpha.com/v1/result?i={expression}&appid={wolframID}")
    
    # return result
    valid = not (s.content == b'Wolfram|Alpha did not understand your input')
    short = not (s.content == b'No short answer available')
    response = {"result": str(s.content)[2:-1]} if (valid and short) else {"result": "can't evaluate"}
    return jsonify(response)

# Home route
# Renders a page that requests the /api route
@app.route('/')
def home():
    return render_template("home.html", example=examples[random.randint(0, len(examples) - 1)]) # Fixes jinja2 replacement of message for Vue.js

# Handle 404
@app.errorhandler(404)
def not_found(e):
    return render_template("error.html", error="404")

# Handle 500
@app.errorhandler(500)
def internal_error(e):
    return render_template("error.html", error="500")