"""
Flask API for AI Content Generator - Optimized for Render.com
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from main import SimpleContentGenerator
import os

app = Flask(__name__)

# CORS configuration
CORS(app, resources={
    r"/*": {
        "origins": ["*"],  # Allow all origins for simplicity
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Initialize generator
generator = SimpleContentGenerator()

@app.route('/')
def home():
    return jsonify({
        "service": "AI Content Generator API",
        "version": "2.0.0",
        "status": "running",
        "endpoints": {
            "GET /health": "Health check",
            "POST /generate": "Generate content",
            "GET /generate?topic=xxx": "Generate via GET"
        },
        "deployed_on": "Render.com",
        "note": "This API generates human-like, SEO-friendly content"
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "AI Content Generator",
        "timestamp": __import__('datetime').datetime.now().isoformat()
    })

@app.route('/generate', methods=['GET', 'POST', 'OPTIONS'])
def generate_content():
    if request.method == 'OPTIONS':
        # Handle preflight requests
        return '', 200
    
    try:
        # Get input data
        if request.method == 'POST':
            if request.is_json:
                data = request.get_json()
            else:
                data = request.form.to_dict()
        else:  # GET request
            data = {
                'topic': request.args.get('topic', ''),
                'keywords': request.args.get('keywords', ''),
                'tone': request.args.get('tone', 'professional'),
                'length': request.args.get('length', '500')
            }
        
        # Validate required fields
        if not data.get('topic'):
            return jsonify({
                'success': False,
                'error': 'Topic is required. Please provide a topic for content generation.'
            }), 400
        
        # Convert length to integer
        try:
            length = int(data.get('length', 500))
            length = max(100, min(2000, length))  # Limit between 100-2000 words
        except:
            length = 500
        
        # Generate content
        result = generator.generate_content(
            topic=data['topic'].strip(),
            keywords=data.get('keywords', '').strip(),
            tone=data.get('tone', 'professional').strip(),
            length=length
        )
        
        return jsonify(result)
        
    except Exception as e:
        # Log error
        print(f"Error generating content: {str(e)}")
        
        return jsonify({
            'success': False,
            'error': f'An error occurred while generating content: {str(e)}',
            'tip': 'Please try again with a different topic or shorter length.'
        }), 500

@app.route('/batch', methods=['POST'])
def batch_generate():
    """Generate content for multiple topics"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        topics = data.get('topics', [])
        
        if not topics:
            return jsonify({
                'success': False,
                'error': 'No topics provided'
            }), 400
        
        if len(topics) > 10:
            return jsonify({
                'success': False,
                'error': 'Maximum 10 topics allowed per request'
            }), 400
        
        results = []
        for topic in topics:
            if isinstance(topic, dict):
                # If topic is an object with additional params
                result = generator.generate_content(
                    topic=topic.get('topic', ''),
                    keywords=topic.get('keywords', ''),
                    tone=topic.get('tone', 'professional'),
                    length=int(topic.get('length', 300))
                )
            else:
                # If topic is just a string
                result = generator.generate_content(
                    topic=str(topic),
                    keywords=data.get('keywords', ''),
                    tone=data.get('tone', 'professional'),
                    length=int(data.get('length', 300))
                )
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

@app.route('/seo-analyze', methods=['POST'])
def seo_analyze():
    """Analyze SEO of provided content"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': 'Content-Type must be application/json'
            }), 400
        
        data = request.get_json()
        content = data.get('content', '')
        
        if not content:
            return jsonify({
                'success': False,
                'error': 'Content is required for SEO analysis'
            }), 400
        
        # Simple SEO analysis
        from nltk.tokenize import word_tokenize, sent_tokenize
        
        words = word_tokenize(content)
        sentences = sent_tokenize(content)
        
        analysis = {
            'word_count': len(words),
            'sentence_count': len(sentences),
            'avg_words_per_sentence': round(len(words) / len(sentences), 2) if sentences else 0,
            'heading_count': content.count('#'),
            'paragraph_count': content.count('\n\n') + 1,
            'link_count': content.count('http'),
            'readability': 'Good' if len(sentences) > 0 and (len(words) / len(sentences)) < 25 else 'Could be improved'
        }
        
        return jsonify({
            'success': True,
            'analysis': analysis,
            'recommendations': [
                'Aim for 300+ words for better SEO',
                'Use 2-3 headings to structure content',
                'Include relevant keywords naturally',
                'Add external links for credibility'
            ]
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found. Please check the API documentation.'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'error': 'Method not allowed for this endpoint.'
    }), 405

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting AI Content Generator API on port {port}...")
    print("Ready to generate content!")
    
    # Note: For production on Render, use gunicorn
    # Command: gunicorn api:app
    app.run(host='0.0.0.0', port=port, debug=False)
