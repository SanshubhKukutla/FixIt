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
    message["Subject"] = "Test email from Python Flask Server"
    message.attach(MIMEText("This is a test email sent from Python running in a Flask server.", "plain"))
    
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

@app.route('/get_data', methods=['GET'])
def get_image():
    document = collection.find_one()
    return jsonify(document['image']) if document else jsonify({'message': 'No document found'})

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


@app.route('/', methods=['GET'])
def test():
    return "HI"
# Start Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5111)
