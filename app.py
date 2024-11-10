import openai
from flask import Flask, jsonify, request, make_response
from flask_cors import CORS

import os
import bleach

app = Flask(__name__)
CORS(app)

@app.route('/api/v1/submit-form', methods=['POST', 'OPTIONS'])
def submit_form():
    if request.method == 'OPTIONS':
        # Handle CORS preflight request
        response = make_response()
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    # Process the POST request
    try:
        data = request.get_json()
        print(type(data))
        print(str(data))

        # Example: Sanitize input data
        sanitized_items = [bleach.clean(item) for item in data.get('items', [])]
        sanitized_allergens = [bleach.clean(a) for a in data.get('allergens', [])]
        
        # TODO: Add your logic here (e.g., store data, interact with other services)

        # Return a success response
        return jsonify({
            "message": "Form submitted successfully!",
            "data": {
                "items": sanitized_items,
                "allergens": sanitized_allergens
            }
        }), 200

    except Exception as e:
        print(f"Error processing form submission: {e}")
        # Return an error response
        return jsonify({
            "message": "An error occurred while processing the form.",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8001')