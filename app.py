from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from model import run_inference
from report_generator import generate_report
from database import insert_result
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Ensure upload and report folders exist
os.makedirs("static/uploads", exist_ok=True)
os.makedirs("static/reports", exist_ok=True)

@app.route('/')
def index():
    return 'Deepfake Detection Backend Running'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = file.filename
    file_path = os.path.join('static', 'uploads', filename)
    file.save(file_path)

    try:
        result, confidence = run_inference(file_path)
    except Exception as e:
        return jsonify({"error": f"Error analyzing file: {str(e)}"}), 500

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report_filename = f"{os.path.splitext(filename)[0]}_report.pdf"

    try:
        generate_report(result, confidence, report_filename, timestamp)
    except Exception as e:
        return jsonify({"error": f"Error generating report: {str(e)}"}), 500

    try:
        insert_result(filename, result, confidence, timestamp)
    except Exception as e:
        print("⚠️ Warning: Could not insert to database.", str(e))

    return jsonify({
        "label": result,
        "confidence": confidence,
        "report_url": f"/static/reports/{report_filename}"
    })

@app.route('/static/reports/<path:filename>', methods=['GET'])
def download_report(filename):
    return send_from_directory("static/reports", filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
