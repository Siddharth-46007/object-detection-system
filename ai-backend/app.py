from flask import Flask, request, jsonify, send_file
import cv2
import torch
from ultralytics import YOLO
import numpy as np
from PIL import Image
import os
import json
import time
import uuid

app = Flask(__name__)

# Load YOLO model
model_path = 'models/yolov8n.pt'
model = None

def load_model():
    global model
    try:
        model = YOLO(model_path)
        print("YOLO model loaded successfully")
    except Exception as e:
        print(f"Error loading model: {e}")
        # Download YOLOv8 nano model if not exists
        model = YOLO('yolov8n.pt')
        print("Downloaded and loaded YOLOv8n model")

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "ai-backend"}), 200

@app.route('/predict', methods=['POST'])
def predict():
    try:
        start_time = time.time()
        
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        file = request.files['image']
        
        # Read image
        image = Image.open(file.stream)
        image_np = np.array(image)
        
        # Run inference
        results = model(image_np)
        
        # Process results
        detections = []
        annotated_image = image_np.copy()
        
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    # Get box coordinates
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    confidence = box.conf[0].cpu().numpy()
                    class_id = int(box.cls[0].cpu().numpy())
                    class_name = model.names[class_id]
                    
                    # Add to detections
                    detections.append({
                        'class': class_name,
                        'confidence': float(confidence),
                        'bbox': {
                            'x1': float(x1),
                            'y1': float(y1),
                            'x2': float(x2),
                            'y2': float(y2)
                        }
                    })
                    
                    # Draw bounding box
                    cv2.rectangle(annotated_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    
                    # Add label
                    label = f'{class_name}: {confidence:.2f}'
                    cv2.putText(annotated_image, label, (int(x1), int(y1) - 10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        # Save annotated image
        output_filename = f'output_{uuid.uuid4().hex}.jpg'
        output_path = os.path.join('outputs', output_filename)
        cv2.imwrite(output_path, cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
        
        # Save JSON results
        json_filename = output_filename.replace('.jpg', '.json')
        json_path = os.path.join('outputs', json_filename)
        
        result_data = {
            'detections': detections,
            'image_filename': output_filename,
            'processing_time': time.time() - start_time,
            'total_objects': len(detections)
        }
        
        with open(json_path, 'w') as f:
            json.dump(result_data, f, indent=2)
        
        return jsonify({
            'success': True,
            'detections': detections,
            'image_with_boxes': output_filename,
            'json_file': json_filename,
            'processing_time': result_data['processing_time'],
            'total_objects': len(detections)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join('outputs', filename)
        if os.path.exists(file_path):
            return send_file(file_path)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.makedirs('outputs', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    
    load_model()
    app.run(host='0.0.0.0', port=5001, debug=True)