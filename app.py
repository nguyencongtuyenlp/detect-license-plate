import os
import cv2
import base64
import numpy as np
from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io

app = Flask(__name__)

# 1. Load Model
model = YOLO('best.pt')

# Config folders
UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Save original
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # YOLO Inference
    results = model(filepath)
    
    # Process results
    res_plotted = results[0].plot()
    result_image = Image.fromarray(res_plotted[..., ::-1])
    
    result_filename = 'result_' + file.filename
    result_path = os.path.join(UPLOAD_FOLDER, result_filename)
    result_image.save(result_path)

    return jsonify({
        'uploaded_image': filepath,
        'result_image': result_path
    })

@app.route('/predict_realtime', methods=['POST'])
def predict_realtime():
    data = request.get_json()
    if 'image' not in data:
        return jsonify({'error': 'No image data'}), 400

    # Decode base64 image
    img_data = base64.b64decode(data['image'].split(',')[1])
    nparr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # YOLO Inference
    results = model(img)

    # Draw results
    res_plotted = results[0].plot()
    
    # Encode back to base64
    _, buffer = cv2.imencode('.jpg', res_plotted)
    res_base64 = base64.b64encode(buffer).decode('utf-8')

    return jsonify({
        'result_image': 'data:image/jpeg;base64,' + res_base64
    })

if __name__ == '__main__':
    # Cổng mặc định là 5000 cho máy local, 7860 cho Hugging Face Spaces
    port = int(os.environ.get("PORT", 5000))
    if port == 5000: # Nếu chạy local thì mở port 5000
        app.run(debug=True, host='0.0.0.0', port=5000)
    else: # Nếu chạy trên Cloud (Hugging Face)
        app.run(host='0.0.0.0', port=port)
