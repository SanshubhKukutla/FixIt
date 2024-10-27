from flask import Flask, request, jsonify
from datetime import datetime
from flask_cors import CORS
from pymongo import MongoClient
import base64

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Connect to MongoDB using your connection string
client = MongoClient('mongodb+srv://arnavt2955:MryIVYfDzpDvxY9Z@cluster0.z8wnd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['imagedb']
collection = db['images']

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)