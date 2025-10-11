from flask import Flask, render_template, request, jsonify, redirect, url_for
import requests
import json
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Backend API URL
BACKEND_URL = "http://localhost:8000/api"

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/upload-file', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file selected'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Send to backend for processing
        try:
            with open(filepath, 'rb') as f:
                files = {'file': (filename, f, 'application/pdf')}
                response = requests.post(f"{BACKEND_URL}/upload-pdf/", files=files)
            
            if response.status_code == 200:
                result = response.json()
                return jsonify({
                    'success': True,
                    'message': 'File uploaded and processed successfully',
                    'data': result
                })
            else:
                return jsonify({'error': 'Backend processing failed'}), 500
                
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            # Clean up uploaded file
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/query')
def query():
    return render_template('query.html')

@app.route('/search-transactions', methods=['POST'])
def search_transactions():
    data = request.json
    try:
        response = requests.post(f"{BACKEND_URL}/search-transactions/", json=data)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/results')
def results():
    return render_template('results.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)