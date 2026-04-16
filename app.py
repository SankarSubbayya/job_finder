"""Flask web application for Job Finder Agent."""

from flask import Flask, render_template, request, jsonify, send_file
import os
import json
from pathlib import Path
from werkzeug.utils import secure_filename
from impl import run_job_finder, export_to_json

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads folder if it doesn't exist
Path(app.config['UPLOAD_FOLDER']).mkdir(exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}


def allowed_file(filename):
    """Check if file is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/api/search', methods=['POST'])
def search_jobs():
    """Search for jobs based on uploaded resume."""
    if 'resume' not in request.files:
        return jsonify({'error': 'No resume file provided'}), 400

    file = request.files['resume']

    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400

    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Get optional parameters
        job_title = request.form.get('job_title')
        location = request.form.get('location')

        # Run job finder with optional parameters
        result = run_job_finder(filepath, job_title=job_title, location=location)

        # Clean up uploaded file
        os.remove(filepath)

        if 'error' in result:
            return jsonify({'error': result['error']}), 500

        return jsonify({
            'success': True,
            'summary': result.get('summary', ''),
            'results': result.get('results', ''),
            'total_matches': result.get('total_matches', 0),
            'matched_jobs': result.get('matched_jobs', []),
            'resume_info': result.get('resume_info', {})
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export', methods=['POST'])
def export_results():
    """Export results as JSON."""
    try:
        data = request.json
        output_path = 'job_matches.json'

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        return send_file(output_path, as_attachment=True, download_name='job_matches.json')

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})


if __name__ == '__main__':
    app.run(debug=True, port=5000)
