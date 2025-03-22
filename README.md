# **TikTok Watermark Removal Project**

This project provides a solution to remove TikTok watermarks from videos by detecting and blurring the watermark. It utilizes computer vision techniques and FFmpeg for audio extraction and video processing. The project includes a FastAPI backend for video processing, along with a React Native frontend to interact with the backend.

---

## **Features**

- **Watermark Detection**: Detects TikTok watermark in video frames using ORB (Oriented FAST and Rotated BRIEF) feature matching.
- **Watermark Removal**: Once detected, the watermark is blurred using Gaussian blur.
- **Audio Extraction**: Extracts audio from the video and combines it with the processed video.
- **FastAPI Backend**: A RESTful API built with FastAPI to upload and process videos.
- **React Native Frontend**: A simple mobile interface for uploading videos and receiving processed output.

---

## **Installation**

### 1. **Clone the Repository**

```bash
git clone https://github.com/your-username/tiktok-watermark-removal.git
cd tiktok-watermark-removal
```

### 2. Set Up Backend (FastAPI)

The backend uses FastAPI and FFmpeg to process videos.

Install dependencies for the backend:

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

In order for the app to be able to find and access the API, I used my IP address as the host on port 8000. Here is the command I ran.

```bash
uvicorn main:app --reload --host $(ipconfig getifaddr en0) --port 8000
```

#### FFmpeg Installation:

Ensure that FFmpeg is installed on your system. Follow the instructions for your platform:

**Using Homebrew**

```bash
brew install ffmpeg
```

**Ubuntu/Linux**

```bash
sudo apt update && sudo apt install ffmpeg
```

**Windows**

1. Download FFmpeg from ffmpeg.org.
2. Add the `bin` folder of FFmpeg to your system `PATH`.

Run the FastAPI server:

```bash
uvicorn main:app --reload --host $(ipconfig getifaddr en0) --port 8000
```

Get the output for the host (your IP), we will need this for later.

The backend should now be running at http://<your IP address>:8000.

### 3. Set Up Frontend (React Native)

The frontend is a mobile app built with React Native.

Install dependencies for the frontend:

```bash
cd frontend
npm install
```

### Accessing the API

Navigate to the `Document.jsx` component under `components`, find line 16.

```javascript
useEffect(() => {
  const fetchLocalIP = async () => {
    const ip = await Network.getIpAddressAsync();
    setAPI_URL(`http://<put your IP address here>:8000`);
  };
  fetchLocalIP();
}, []);
```

You must put the API address in this line before trying to run locally. Save this change, then proceed (I will fix this later).

I used expo to develop this app, so I used this command to run.

```bash
npx expo start
```

You should now be able to open the app on a simulator or device.

[React Native offical documentation](https://reactnative.dev/docs/getting-started)

---

## Usage

### 1. Upload a Video

    Open the React Native app.
    Tap on Upload MP4 to select a TikTok video with a watermark.
    The app will upload the video to the backend for processing.

### 2. Detect Watermark and Process Video

    After uploading, the backend will process the video:
        It will detect the watermark.
        If the watermark is found, it will blur the watermark area.
        The audio from the video will be extracted and combined with the processed video.

### 3. Download the Processed Video

    Once the video is processed, the app will display a Download Video button.
    Tap the button to download the processed video without the watermark.

---

## API Endpoints

### 1. `POST /upload/`

Upload a video to be processed.

Request:

`file`: The video file to be uploaded (MP4 format).

Response:

```json
{
  "filename": "your-video.mp4",
  "watermark": true,
  "download_url": "/download/processed_your-video.mp4"
}
```

### 2. `GET /download/{filename}`

Download the processed video after watermark removal.

Response:

    The processed video file.

---

## Assumptions

1. Video Format:
   The project assumes that the video format is MP4, as this is a common format for TikTok videos and ensures compatibility with FFmpeg and OpenCV for processing.

2. Video Quality:
   The effectiveness of watermark detection depends on the video quality. Videos with very low resolution or extremely high compression may not detect the watermark as reliably.

3. No Interactive Editing:
   The user can upload videos to the system, but they cannot manually interact with or select specific frames of the video for watermark removal. The process is fully automated.

---

## Why These Choices Were Made

### **Why I Chose Expo for the Frontend**

As this is my first mobile app development project, I wanted to choose a framework that would allow me to build the app quickly and with less complexity. I decided to use Expo for:
_ Ease of use
_ Quick development and testing
_ Cross-platform compatibility
_ Documentation Focus on React Native

By using Expo, I was able to quickly create a functioning mobile app without getting bogged down by the complexities of native mobile development. It helped me focus on the core features of the app, and I was able to learn and experiment with mobile app development efficiently.

---

## **About My Experience as a Beginner**

As a beginner, this is my first mobile app. I wanted to learn how to build an app that interacts with a backend server and allows users to upload, process, and download videos. Expo and React Native gave me the tools to accomplish this, and while it came with challenges, it has been a great learning experience. I am excited to continue improving my skills and creating more sophisticated mobile apps in the future.

1. Why FastAPI for the Backend?

   - Performance: FastAPI offers high performance for building APIs, which is essential for handling video processing requests efficiently.
   - Async Support: FastAPI allows asynchronous request handling, which improves the response time for large video file uploads and processing.

2. Why ORB for Watermark Detection?

   - Efficiency: ORB is a fast and efficient feature matching algorithm that works well for detecting fixed watermarks, like the TikTok logo, in videos.
   - OpenCV Integration: ORB is natively supported by OpenCV, which is already being used for video processing in the project.

3. Why FFmpeg for Audio Extraction and Video Merging?

   - Industry Standard: FFmpeg is widely used for video and audio processing due to its flexibility and powerful feature set.
   - Ease of Integration: FFmpeg is simple to integrate into Python projects using either subprocess or the ffmpeg-python wrapper. It handles the audio extraction and merging seamlessly.

4. Why React Native for the Frontend?
   - Cross-Platform: React Native allows for building apps that can run on both iOS and Android using the same codebase, which helps in quickly reaching a wider audience.
   - Community Support: React Native has a large community, meaning it is easier to find support and resources for building the frontend.

---

## **Future Improvements**

While the current version of the TikTok watermark removal project effectively detects and removes watermarks using ORB feature matching and Gaussian blur, there are several improvements that could make the system more robust and scalable:

### 1. **Switching to YOLO for Watermark Detection**

- **Current Method**: The project currently uses **ORB feature matching** to detect TikTok watermarks. While this method works for many cases, it may struggle with videos that have significant noise, scaling, or rotation in the watermark position.

- **Improvement**: One of the major improvements I plan to implement is switching to a **YOLO (You Only Look Once) model**, such as **YOLOv4**, for watermark detection. YOLO is a real-time object detection model that can perform better in various conditions such as:

  - **Robustness to Scaling**: YOLO can detect objects (like a watermark) at different scales and sizes, which is important as TikTok watermarks can appear in various locations and sizes across different videos.
  - **Speed and Accuracy**: YOLO is well-known for being fast while maintaining high accuracy, making it a great choice for real-time watermark detection in videos.

- **Implementation**: I will train a YOLOv4 model specifically for watermark detection, or alternatively, use a pre-trained model fine-tuned for this task. Once implemented, YOLO will be used to detect the watermark in each frame, and the detection results will be used to blur the watermark region in the video.

- **Benefits**:
  - Increased accuracy in detecting watermarks.
  - Better handling of dynamic changes in video content.
  - Reduced reliance on feature matching techniques that may fail under certain conditions.

### 2. **Making the API More Accessible and Scalable**

- **Current API Setup**: The current API is built using **FastAPI**, and it provides a straightforward mechanism for uploading and processing videos. However, the API could be more accessible and scalable for production use.

- **Improvement 1 - CORS and Authentication**: To make the API more accessible for different clients, I plan to:

  - **Implement Authentication**: Adding basic **API key authentication** or OAuth to restrict access and ensure that only authorized users can upload and process videos.
  - **Handle CORS Better**: Allow more configurable cross-origin resource sharing (CORS) to ensure that the API can be used seamlessly with a variety of clients (e.g., mobile, web apps) across different domains.

- **Improvement 2 - Asynchronous Video Processing**: While FastAPI already supports asynchronous tasks, video processing tasks can still be time-consuming, especially with high-resolution videos. To address this:

  - **Queue-based System**: Implement a task queue (e.g., **Celery** with **Redis** or **RabbitMQ**) to handle video processing asynchronously. This will help improve the API’s responsiveness by processing videos in the background and notifying users when their video is ready.
  - **Real-time Progress Tracking**: Implement real-time tracking for the video processing task, allowing users to track the status of their video in real-time, reducing wait time anxiety and improving user experience.

- **Improvement 3 - API Rate Limiting**: Introduce **rate-limiting** for the API to prevent abuse and ensure fair usage, especially when scaling the API for public use.

- **Improvement 4 - Cloud Hosting**: For scalability, I plan to host the API on a cloud service like **AWS**, **Google Cloud**, or **Azure**. This will allow the system to scale dynamically depending on demand, handle large file uploads, and serve users from multiple regions.

- **Improvement 5 - Documentation and SDK**: To make the API more user-friendly and easier to integrate with other platforms, I plan to:
  - **Generate Comprehensive API Docs**: Use **Swagger** (which FastAPI already supports) to generate detailed API documentation, including usage examples, request/response formats, and authentication methods.
  - **SDK Development**: Create SDKs (software development kits) in multiple languages (e.g., Python, JavaScript) that allow developers to easily interact with the API without having to manually make HTTP requests.

---

### **Benefits of These Improvements**

- **Better Detection Accuracy**: Switching to a YOLOv4-based detection model will result in more accurate watermark detection, especially in challenging video conditions.
- **Enhanced API Scalability**: The improvements in API infrastructure (asynchronous processing, authentication, and scaling) will allow the project to handle a larger user base and provide a more reliable service.
- **Increased Flexibility and Usability**: By improving API accessibility and adding user-friendly features like real-time progress tracking, the system will be easier to use and integrate with other services.
- **Better Cloud Integration**: Hosting the API on the cloud will improve performance, scalability, and redundancy, ensuring that the service can handle more requests and provide faster video processing.

---

## Technologies Used

    FastAPI: For the backend server to process videos.
    OpenCV: For watermark detection using ORB feature matching.
    FFmpeg: For audio extraction and video merging.
    React Native: For the mobile frontend.
    Python: Backend language.
    JavaScript: Frontend language.
