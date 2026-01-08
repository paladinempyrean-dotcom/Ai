#!/usr/bin/env python3
"""
Test script to verify AI Image Analyzer setup
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8+"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is installed")
        return True
    else:
        print(f"❌ Python 3.8+ required, but found {version.major}.{version.minor}.{version.micro}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    print("\nChecking dependencies...")
    dependencies = [
        'flask',
        'flask_cors',
        'cv2',
        'numpy',
        'PIL'
    ]
    
    all_installed = True
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} is installed")
        except ImportError:
            print(f"❌ {dep} is NOT installed")
            all_installed = False
    
    return all_installed

def check_opencv_cascades():
    """Check if OpenCV cascades are available"""
    print("\nChecking OpenCV cascade files...")
    try:
        import cv2
        cascades = [
            'haarcascade_frontalface_default.xml',
            'haarcascade_eye.xml',
            'haarcascade_smile.xml'
        ]
        
        all_found = True
        for cascade in cascades:
            path = cv2.data.haarcascades + cascade
            try:
                with open(path, 'r') as f:
                    print(f"✅ {cascade} found")
            except FileNotFoundError:
                print(f"❌ {cascade} NOT found")
                all_found = False
        
        return all_found
    except Exception as e:
        print(f"❌ Error checking cascades: {e}")
        return False

def test_basic_functionality():
    """Test basic image processing"""
    print("\nTesting basic functionality...")
    try:
        import cv2
        import numpy as np
        
        # Create a test image
        img = np.zeros((100, 100, 3), dtype=np.uint8)
        print("✅ Can create test image")
        
        # Test grayscale conversion
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print("✅ Can convert to grayscale")
        
        # Test cascade loading
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        print("✅ Can load face cascade")
        
        return True
    except Exception as e:
        print(f"❌ Error in basic functionality test: {e}")
        return False

def check_flask_setup():
    """Check if Flask app can be imported"""
    print("\nChecking Flask application...")
    try:
        from app import app, ai
        print("✅ Flask app imported successfully")
        print(f"✅ AI analyzer initialized")
        return True
    except Exception as e:
        print(f"❌ Error importing Flask app: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("AI Image Analyzer - Setup Verification")
    print("=" * 50)
    
    results = []
    
    results.append(("Python Version", check_python_version()))
    results.append(("Dependencies", check_dependencies()))
    results.append(("OpenCV Cascades", check_opencv_cascades()))
    results.append(("Basic Functionality", test_basic_functionality()))
    results.append(("Flask Setup", check_flask_setup()))
    
    print("\n" + "=" * 50)
    print("Test Summary")
    print("=" * 50)
    
    all_passed = True
    for test_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if not passed:
            all_passed = False
    
    print("=" * 50)
    
    if all_passed:
        print("\n🎉 All tests passed! Your setup is ready.")
        print("\nTo run the application:")
        print("  python app.py")
        print("\nThen open your browser to:")
        print("  http://localhost:5000")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please install missing dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())
