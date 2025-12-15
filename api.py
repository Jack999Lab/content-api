"""
Flask API for AI Content Generator
Deploy on: Replit, Railway, Render, PythonAnywhere
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from main import SimpleAIGenerator

app = Flask(__name__)
CORS(app)  # Allow all origins

# Initialize generator
generator = SimpleAIGenerator()

@app.route('/')
def home():
    return jsonify({
        "service": "AI Content Generator API",
        "version": "1.0.0",
        "endpoints": {
            "/generate": "POST - Generate content",
            "/health": "GET - Health check"
        },
        "usage": 'Send POST request to /generate with JSON: {"topic":"Your Topic","keywords":"kw1,kw2"}'
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "service": "AI Content Generator"})

@app.route('/generate', methods=['POST', 'GET'])
def generate():
    try:
        # Get input data
        if request.method == 'POST':
            data = request.get_json()
        else:
            # For GET requests with query parameters
            data = {
                'topic': request.args.get('topic', ''),
                'keywords': request.args.get('keywords', ''),
                'tone': request.args.get('tone', 'professional'),
                'length': request.args.get('length', 500)
            }
        
        # Validate
        if not data.get('topic'):
            return jsonify({
                'success': False,
                'error': 'Topic is required'
            }), 400
        
        # Generate content
        result = generator.generate_content(
            topic=data['topic'],
            keywords=data.get('keywords', ''),
            tone=data.get('tone', 'professional'),
            length=int(data.get('length', 500))
        )
        
        # Add success flag
        result['success'] = True
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/batch', methods=['POST'])
def batch_generate():
    """Multiple topics at once"""
    try:
        data = request.get_json()
        topics = data.get('topics', [])
        
        if not topics or len(topics) > 10:
            return jsonify({
                'success': False,
                'error': 'Provide 1-10 topics'
            }), 400
        
        results = []
        for topic in topics:
            result = generator.generate_content(
                topic=topic,
                keywords=data.get('keywords', ''),
                tone=data.get('tone', 'professional'),
                length=int(data.get('length', 300))
            )
            result['topic'] = topic
            results.append(result)
        
        return jsonify({
            'success': True,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Run the server
    print("Starting AI Content Generator API...")
    print("Endpoint: http://localhost:5000")
    print("Press Ctrl+C to stop")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=False  # Set to False in production
    )