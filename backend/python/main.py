import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import websockets
from threading import Thread
from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from pymongo import MongoClient
import base64, os
from dotenv import load_dotenv
import random
import anthropic
import base64
import PIL.Image
import PIL.ImageDraw
import base64
from io import BytesIO
from PIL import Image

history = []


def run_claude(image, prompt):
    client = anthropic.Anthropic(api_key="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")
    image_data = image
    image_media_type = "image/png"
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": image_media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt
                    }
                ],
            }
        ],
    )
    return message.content[0].textfrom flask import Flask, request, jsonify, send_from_directory
import os
from flask import Flask, request, jsonify
import base64
import requests


# Initialize Flask app
app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={r"/api/*": {"origins": "*", "methods": ["POST", "GET", "OPTIONS"], "allow_headers": ["Content-Type"]}})

# Store clients connected to WebSocket
clients = set()
load_dotenv()

MONGO = os.getenv('MONGO')
EMAILPWD = os.getenv("emailpwd")

# Connect to MongoDB using your connection string
client = MongoClient(MONGO)
db = client['imagedb']
collection = db['images']

# Email sending function
def send_email():
    sender_email = "arnavtripathi@gmail.com"
    receiver_email = "royceaden@gmail.com"
    password = EMAILPWD
    
    # Create email message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = "Python Server Email"
    message.attach(MIMEText("DEMO LINK: https://fixit.pleom.com/ar-code/ar.html", "plain"))
    
    try:
        # Send email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(message)
        return {"status": "Email sent successfully"}
    except Exception as e:
        return {"status": f"Error sending email: {str(e)}"}

# WebSocket server function
async def websocket_server(websocket, path):
    clients.add(websocket)
    try:
        while True:
            await websocket.recv()
    except websockets.exceptions.ConnectionClosed:
        clients.remove(websocket)

# Broadcast message to all WebSocket clients
async def broadcast_message(message):
    if clients:
        await asyncio.gather(*[client.send(json.dumps(message)) for client in clients])

# WebSocket server setup and loop
def run_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(
        websocket_server, "localhost", 8765,
        extra_headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )
    loop.run_until_complete(start_server)
    loop.run_forever()

# Start WebSocket server in separate thread
Thread(target=run_websocket_server, daemon=True).start()

# API route to receive and broadcast data
@app.route('/api/data', methods=['GET'])
def receive_data():
    data = request.json
    asyncio.run(broadcast_message(data))
    return jsonify({"status": "success"})

# API route to send email
@app.route('/send-email', methods=['POST'])
def email():
    response = send_email()
    return jsonify(response)

@app.route('/process_image', methods=['POST'])
def process_image():
    data = request.json
    image_data = data.get("image")
    
    # Decode the base64 image
    image_binary = base64.b64decode(image_data)
    
    # Here you would call your Gemini API or any processing function
    # For example, sending the image to the Gemini API:
    try:
        url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer AIzaSyAg216xspoLnCCe1Xn8vRsGw7xk-A76wd4"  # Directly include the API key without additional {}
        }

        payload = {"image": image_data}

        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get_data', methods=['GET'])
@app.route('/get_data', methods=['POST'])
def get_image():

    global history
    data = request.json
    print(data)

    current_step = 1
    current_prompt = "user said this"
    prompt = f"""
    You are given an image of an instructional manual which contains four steps ordered from top to bottom. The user is currently on {current_step}.
    You 

    The user recently said the following: {current_prompt}
    The user also said the following previously as well. {" ".join(history)}
    """

    print(data)
    '''
    image = PIL.Image.open("image.png")
    with open("image.png", "rb") as image_file:
        image_data = base64.b64encode(image_file.read()).decode('utf-8')
        output = run_claude(image_data, prompt)
        return output
    '''
    history.append(current_prompt) 
    return jsonify({"body": {
        "instructions": "okay it's because you did not screw it in properly"
    }}), 200
@app.route('/upload_image', methods=['POST'])
def upload_image():
    try:
        collection.delete_many({})  
        base64_image = request.json['image']
        
        # Create document to insert
        document = {
            "image": base64_image,
            "timestamp": datetime.utcnow()
        }
        
        # Insert the document
        result = collection.insert_one(document)
        
        return jsonify({"insertedId": str(result.inserted_id)}), 200
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500
@app.route('/')
def serve_index():
    print("Serving index.html from:", os.path.abspath('.'))
    return send_from_directory('.', 'index.html')

@app.route('/', methods=['GET'])
def test():
    return "Our Server"

# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5122, debug=True)
