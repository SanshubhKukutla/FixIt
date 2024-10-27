from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
import websockets
import json
from threading import Thread

app = Flask(__name__)
# Enable CORS for all routes
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # Allow all origins
        "methods": ["POST", "GET", "OPTIONS"],  # Allowed methods
        "allow_headers": ["Content-Type"]  # Allowed headers
    }
})

clients = set()

async def websocket_server(websocket, path):
    clients.add(websocket)
    try:
        while True:
            await websocket.recv()
    except websockets.exceptions.ConnectionClosed:
        clients.remove(websocket)

async def broadcast_message(message):
    if clients:
        await asyncio.gather(
            *[client.send(json.dumps(message)) for client in clients]
        )

def run_websocket_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    start_server = websockets.serve(
        websocket_server, 
        "localhost", 
        8765,
        # Add CORS headers for WebSocket connections
        extra_headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type"
        }
    )
    loop.run_until_complete(start_server)
    loop.run_forever()

Thread(target=run_websocket_server, daemon=True).start()

@app.route('/api/data', methods=['POST'])
def receive_data():
    data = request.json
    asyncio.run(broadcast_message(data))
    return jsonify({"status": "success"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)