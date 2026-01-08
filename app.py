from flask import Flask, render_template, request, jsonify, Response
from flask_cors import CORS
import cv2
import numpy as np
from PIL import Image
import io
import base64
import json
from datetime import datetime

app = Flask(__name__)
CORS(app)

class ImageAnalyzerAI:
    def __init__(self):
        # Initialize face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
        self.smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
        
        # Initialize object detection (using MobileNet SSD)
        self.net = None
        try:
            # You'll need to download these files
            # https://github.com/opencv/opencv/blob/master/samples/dnn/face_detector/deploy.prototxt
            # https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel
            pass
        except:
            print("Deep learning models not loaded. Using basic detection only.")
    
    def analyze_image(self, image_data):
        """Analyze image and return description of what's happening"""
        try:
            # Convert base64 to image
            if 'base64,' in image_data:
                image_data = image_data.split('base64,')[1]
            
            image_bytes = base64.b64decode(image_data)
            nparr = np.frombuffer(image_bytes, np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                return {"error": "Could not decode image"}
            
            # Convert to grayscale for detection
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Detect faces
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
            
            # Analyze the scene
            description = self.generate_description(img, gray, faces)
            
            # Draw rectangles on detected objects
            annotated_img = img.copy()
            for (x, y, w, h) in faces:
                cv2.rectangle(annotated_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
                
                # Detect eyes and smile in face region
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = annotated_img[y:y+h, x:x+w]
                
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 255, 0), 2)
                
                smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
                for (sx, sy, sw, sh) in smiles:
                    cv2.rectangle(roi_color, (sx, sy), (sx+sw, sy+sh), (0, 0, 255), 2)
            
            # Convert annotated image back to base64
            _, buffer = cv2.imencode('.jpg', annotated_img)
            annotated_base64 = base64.b64encode(buffer).decode('utf-8')
            
            return {
                "description": description,
                "annotated_image": f"data:image/jpeg;base64,{annotated_base64}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "detections": {
                    "faces": len(faces),
                }
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def generate_description(self, img, gray, faces):
        """Generate natural language description of the image"""
        descriptions = []
        
        # Analyze brightness
        brightness = np.mean(gray)
        if brightness < 85:
            descriptions.append("The scene appears to be in low light or dark conditions.")
        elif brightness > 170:
            descriptions.append("The scene is brightly lit.")
        else:
            descriptions.append("The scene has moderate lighting.")
        
        # Analyze faces
        if len(faces) == 0:
            descriptions.append("No people are detected in the image.")
        elif len(faces) == 1:
            descriptions.append("I can see 1 person in the image.")
            
            # Check for smile in the face region
            for (x, y, w, h) in faces:
                roi_gray = gray[y:y+h, x:x+w]
                smiles = self.smile_cascade.detectMultiScale(roi_gray, 1.8, 20)
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                
                if len(smiles) > 0:
                    descriptions.append("The person appears to be smiling.")
                if len(eyes) >= 2:
                    descriptions.append("Both eyes are visible.")
        else:
            descriptions.append(f"I can see {len(faces)} people in the image.")
        
        # Analyze colors
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        avg_hue = np.mean(hsv[:, :, 0])
        
        if avg_hue < 30:
            descriptions.append("The image has warm tones (reds/oranges).")
        elif avg_hue < 90:
            descriptions.append("The image has yellow/green tones.")
        elif avg_hue < 150:
            descriptions.append("The image has cool blue/cyan tones.")
        
        # Analyze motion/blur (approximate)
        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
        if laplacian_var < 100:
            descriptions.append("The image appears slightly blurry or there may be motion.")
        
        # Check for edges (complexity)
        edges = cv2.Canny(gray, 100, 200)
        edge_density = np.sum(edges > 0) / edges.size
        
        if edge_density > 0.15:
            descriptions.append("The scene contains many details and objects.")
        elif edge_density < 0.05:
            descriptions.append("The scene is relatively simple with few objects.")
        
        return " ".join(descriptions)

# Initialize AI
ai = ImageAnalyzerAI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Analyze uploaded image"""
    try:
        data = request.get_json()
        image_data = data.get('image')
        
        if not image_data:
            return jsonify({"error": "No image provided"}), 400
        
        result = ai.analyze_image(image_data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/webcam-analyze', methods=['POST'])
def webcam_analyze():
    """Analyze webcam frame"""
    try:
        data = request.get_json()
        frame_data = data.get('frame')
        
        if not frame_data:
            return jsonify({"error": "No frame provided"}), 400
        
        result = ai.analyze_image(frame_data)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
