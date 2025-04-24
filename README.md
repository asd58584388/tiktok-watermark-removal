# TikTok Watermark Remover

A full-stack application that detects and removes TikTok watermarks from videos using a fine-tuned YOLOv7 model.

[Watch the demo video](./demo.mp4)

## Project Structure

The project consists of two main components:

- **Frontend**: A mobile app built with Expo and React Native
- **Backend**: A FastAPI server with a YOLOv7 model fine-tuned for TikTok watermark detection and removal

## Technology Decisions

### Model Selection
After evaluating multiple models, YOLOv7 was chosen as the optimal solution for several reasons:
- Good detection accuracy.
- Pre-trained models available, eliminating the need for additional dataset collection and training

### Frontend Architecture
Expo and React Native were selected for the following reasons:
- Cross-platform development (iOS, Android, Web) from a single codebase
- Expo's comprehensive development tools and simplified workflow
- Rich ecosystem of libraries for media handling
- Fast development cycle with hot reloading

### Backend Architecture
FastAPI was chosen as the backend framework for several advantages:
- High performance with async support
- Lightweight and minimal boilerplate code
- Most AI liberaries use python.


## Features

- Upload TikTok videos directly from your device
- Automatic watermark detection using a fine-tuned YOLOv7 model
- Watermark removal while preserving video quality
- Cross-platform support via Expo (iOS, Android, Web)
- Simple and intuitive user interface

## Technology Stack

### Frontend
- [Expo](https://expo.dev/) - React Native framework
- React Native - Mobile app development
- TypeScript - Type-safe JavaScript
- Axios - API communication

### Backend
- [FastAPI](https://fastapi.tiangolo.com/) - High-performance API framework
- YOLOv7 - Computer vision model (fine-tuned for TikTok watermark detection)
- OpenCV - Image and video processing
- ONNX Runtime - Efficient model inference
- Python - Backend programming

## Getting Started

### Prerequisites

- Node.js
- Python 3.12+
- Anaconda or Miniconda
- Git

### Backend Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/asd58584388/tiktok-watermark-removal.git
   cd tiktok-watermark-removal/backend
   ```

2. Create a Conda environment and install dependencies:
   ```bash
   conda create -n tiktok-watermark python=3.12
   conda activate tiktok-watermark
   pip install -r requirements.txt
   ```

3. Start the FastAPI server:
   ```bash
   python start_server.py
   ```
   The server will run on http://localhost:8000 by default.

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd ../frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Configure the API URL:
   - Open `frontend/components/Document.jsx`
   - **IMPORTANT**: Update the `API_URL` in the `fetchLocalIP` function with your server's IP address:
     ```javascript
     // Change this:
     setAPI_URL(`http://192.168.50.77:8000`);
     // To your actual backend server IP address and port
     setAPI_URL(`http://YOUR_SERVER_IP:8000`);
     ```
   - If testing on the same device, you can use `localhost` or `127.0.0.1`
   - For mobile devices on the same network, use your computer's local IP address

4. Start the Expo development server:
   ```bash
   npm start
   ```

5. Use the Expo Go app on your mobile device to scan the QR code, or run on an emulator/simulator.

## Usage

1. Open the app on your device
2. Tap "Upload MP4" to select a TikTok video from your device
3. Tap "Detect Watermark" to process the video
4. If a watermark is detected, a download button will appear
5. Tap "Download" to save the processed video without watermarks

## How It Works

The application uses a YOLOv7 model fine-tuned specifically for TikTok watermark detection. When a video is uploaded:

1. The backend samples frames from the video
2. The model identifies any TikTok watermarks in these frames
3. If watermarks are detected, they are removed using advanced inpainting techniques
4. The processed video is made available for download

## Limitations

- The YOLOv7 model is specifically trained on TikTok logo watermarks and may not perform well with:
  - Text-heavy watermarks
  - Custom text overlays
  - Non-standard watermark placements
  - Watermarks from other platforms


## Future Improvements

### Processing Speed Enhancement**
   - Implement CUDA support for GPU acceleration
   - Optimize video I/O operations

### Model Improvements
   - While YOLOv7 provides good results for watermark detection in most cases, it's not perfect

## Acknowledgments

- The YOLOv7 team for their excellent object detection model
- The FastAPI and Expo communities for their comprehensive documentation
- [Connor Holm's TikTok Watermark YOLOv7](https://github.com/connorholm/tiktok-watermark-yolov7/tree/main/yolov7) for the initial YOLOv7 watermark detection implementation
- [Bridget Bangert's TikTok Watermark Removal](https://github.com/bridgetbangert/tiktok-watermark-removal) for frontend design
