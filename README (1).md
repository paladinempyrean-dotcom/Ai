# 🤖 AI Image Analyzer - Real-time Vision

An intelligent AI-powered application that analyzes images in real-time using computer vision. It can detect faces, analyze emotions, understand scenes, and provide detailed descriptions automatically.

## ✨ Features

- **Real-time Webcam Analysis**: Analyze live video feed from your webcam
- **Face Detection**: Detects and counts people in images
- **Emotion Recognition**: Identifies smiles and facial expressions
- **Scene Understanding**: Analyzes lighting, colors, image complexity, and blur
- **Auto-Analyze Mode**: Automatically analyzes webcam feed every 3 seconds
- **Image Upload**: Analyze any image from your device
- **Visual Annotations**: Draws bounding boxes around detected faces, eyes, and smiles
- **Detailed Descriptions**: Generates natural language descriptions of what's happening in the image

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Webcam (for real-time analysis)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/ai-image-analyzer.git
cd ai-image-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python app.py
```

4. Open your browser and navigate to:
```
http://localhost:5000
```

## 🎯 How to Use

### Webcam Analysis
1. Click **"Start Webcam"** to enable your camera
2. Click **"Analyze Frame"** to analyze the current frame
3. Enable **"Auto-Analyze Mode"** for continuous automatic analysis every 3 seconds

### Upload Image
1. Click **"Upload Image"** button
2. Select an image from your device
3. View the analysis results instantly

## 🔧 Technical Details

### AI Capabilities

The application uses OpenCV's Cascade Classifiers for:
- Face detection (Haar Cascade)
- Eye detection
- Smile detection

Image analysis includes:
- Brightness analysis
- Color tone analysis (HSV)
- Edge detection for scene complexity
- Motion/blur detection (Laplacian variance)

### API Endpoints

- `GET /` - Main interface
- `POST /analyze` - Analyze uploaded image
- `POST /webcam-analyze` - Analyze webcam frame

### Request Format
```json
{
  "image": "data:image/jpeg;base64,..."
}
```

### Response Format
```json
{
  "description": "The scene has moderate lighting. I can see 1 person...",
  "annotated_image": "data:image/jpeg;base64,...",
  "timestamp": "2024-01-08 14:30:00",
  "detections": {
    "faces": 1
  }
}
```

## 🌐 Deployment

### Deploy on Heroku

1. Create a `Procfile`:
```
web: gunicorn app:app
```

2. Create a `runtime.txt`:
```
python-3.11.0
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku open
```

### Deploy on Render

1. Connect your GitHub repository
2. Select "Web Service"
3. Build Command: `pip install -r requirements.txt`
4. Start Command: `gunicorn app:app`

### Deploy on GitHub Pages (Static Version)

For a static version without real-time backend:
1. Create a `docs` folder
2. Move `index.html` to `docs/index.html`
3. Modify to use client-side processing only
4. Enable GitHub Pages in repository settings

## 📁 Project Structure

```
ai-image-analyzer/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Frontend interface
├── static/               # Static files (if needed)
└── README.md            # This file
```

## 🎨 Customization

### Adjust Detection Sensitivity

In `app.py`, modify the cascade parameters:
```python
faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
```
- First parameter (1.3): Scale factor - lower = more sensitive
- Second parameter (5): Min neighbors - lower = more detections

### Change Auto-Analyze Interval

In `index.html`, modify the interval:
```javascript
autoAnalyzeInterval = setInterval(() => {
    captureAndAnalyze();
}, 3000);  // Change 3000 to desired milliseconds
```

## 🔐 Privacy & Security

- All image processing happens locally on your server
- No images are stored permanently
- Webcam access requires user permission
- No data is sent to third-party services

## 🐛 Troubleshooting

**Webcam not working:**
- Ensure browser has camera permissions
- Try using HTTPS (required by some browsers)
- Check if camera is being used by another application

**Detection not accurate:**
- Ensure good lighting conditions
- Face the camera directly
- Adjust detection parameters in code

**Installation errors:**
- Make sure OpenCV is installed correctly
- Try: `pip install opencv-python opencv-contrib-python --upgrade`

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

## 🙏 Acknowledgments

- OpenCV for computer vision capabilities
- Flask for the web framework
- Haar Cascades for object detection

---

Made with ❤️ using Python and OpenCV
