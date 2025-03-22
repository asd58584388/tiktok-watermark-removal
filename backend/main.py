from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
import cv2
import numpy as np
import os
import subprocess

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI server!"}


@app.post("/upload/")
async def upload_video(file: UploadFile = File(...)):
    if os.path.exists(OUTPUT_DIR):
        print("Output directory exists.")
        for filename in os.listdir(OUTPUT_DIR):
            file_path = os.path.join(OUTPUT_DIR, filename)
            
            if os.path.isfile(file_path):
                try:
                    os.remove(file_path)
                    print(f"Deleted file: {file_path}")
                except Exception as e:
                    print(f"Error deleting file {file_path}: {e}")

    try:
        file_path = f"{UPLOAD_DIR}/{file.filename}"
        with open(file_path, "wb") as buffer:
            for chunk in iter(lambda: file.file.read(4096), b""):
                buffer.write(chunk)

        detected = detect_watermark(file_path)
        if detected:
            output_path = os.path.join(OUTPUT_DIR, f"processed_{file.filename}")
            process_video(f"{UPLOAD_DIR}/{file.filename}", output_path)

            return {
                "filename": file.filename,
                "watermark": detected,
                "download_url": f"/download/processed_{file.filename}"
            }
        else:
            return {
                "filename": file.filename,
                "watermark": detected
            }

    except Exception as e:
        return {"error": str(e)}

@app.get("/download/processed_{filename}")
async def download_video(filename: str):
    output_path = os.path.join(OUTPUT_DIR, f"processed_{filename}")
        
    if os.path.exists(output_path):
        return HTMLResponse(content=f"""
            <html>
            <head>
                <title>Download Your Processed Video</title>
                <style>
                    body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                    .container {{ max-width: 600px; margin: auto; padding: 20px; }}
                    .button {{
                        background-color: green;
                        color: white;
                        padding: 10px 20px;
                        text-decoration: none;
                        border-radius: 5px;
                        font-size: 16px;
                        display: inline-block;
                        margin-top: 20px;
                    }}
                    .button:hover {{ background-color: darkgreen; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <h1>Your Video is Ready! 🎉</h1>
                    <p>Click the button below to download your processed video.</p>
                    <a href="/static/processed_{filename}" class="button" download>Download Processed MP4</a>
                </div>
            </body>
            </html>
        """, 
        status_code=200
    )
    else:
        return HTMLResponse(
            content=f"""
                <html>
                <head>
                    <title>File Not Found</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }}
                        .container {{ max-width: 600px; margin: auto; padding: 20px; }}
                        h1 {{ color: red; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>Video is processing...</h1>
                    </div>
                </body>
                </html>
            """,
            status_code=404
        )

@app.get("/static/processed_{filename}")
def serve_processed_video(filename: str):
    output_path = os.path.join(OUTPUT_DIR, f"processed_{filename}")

    if os.path.exists(output_path):
        return FileResponse(output_path, media_type="video/mp4", filename=f"processed_{filename}")
    else:
        return {"error": "File not found"}
    

def detect_watermark(video_path, template_path="tiktok-icon2.png", min_matches=5):
    print("Detecting watermark")

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()
    keypoints_template, descriptors_template = orb.detectAndCompute(template, None)

    cap = cv2.VideoCapture(video_path)
    watermark_detected = False

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        region_width = frame.shape[1] // 8
        left_frame = gray_frame[:, :region_width]
        right_frame = gray_frame[:, -region_width:]

        _, descriptors_left = orb.detectAndCompute(left_frame, None)
        _, descriptors_right = orb.detectAndCompute(right_frame, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        if descriptors_left is not None and descriptors_template is not None:
            matches_left = bf.match(descriptors_template, descriptors_left)
            matches_left = sorted(matches_left, key=lambda x: x.distance)

            if len(matches_left) >= min_matches:
                print("Watermark detected on the **left** side!")
                return True
        
        if descriptors_right is not None and descriptors_template is not None:
            matches_right = bf.match(descriptors_template, descriptors_right)
            matches_right = sorted(matches_right, key=lambda x: x.distance)

            if len(matches_right) >= min_matches:
                print("Watermark detected on the **right** side!")
                return True

    cap.release()
    return watermark_detected

def process_video(video_path, output_path, template_path="tiktok-icon2.png"):
    print("Processing video")
    
    OUTPUT_DIR = os.path.dirname(output_path)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    orb = cv2.ORB_create()

    keypoints_template, descriptors_template = orb.detectAndCompute(template, None)

    cap = cv2.VideoCapture(video_path)
    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    MIN_WIDTH = 100
    MIN_HEIGHT = 100
    prev_box = None
    prev_box_found = False
    prev_frame_count = 0
    MAX_NO_DETECTION_FRAMES = 30
    MIN_MATCHES = 5

    temp_output_path = os.path.join(OUTPUT_DIR, "temp_processed.mp4")

    if os.path.exists(temp_output_path):
        os.remove(temp_output_path)
        print(f"Deleted existing temporary file: {temp_output_path}")

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (frame_width, frame_height))

    audio_path = os.path.join(OUTPUT_DIR, "audio.wav")
    subprocess.run([
        'ffmpeg', '-y', '-i', video_path, '-vn', audio_path
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if os.path.exists(audio_path):
        print(f"Audio file successfully created at: {audio_path}")
    else:
        print(f"Failed to create the audio file from {video_path}.")

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        region_width = frame_width // 8
        left_frame = gray_frame[:, :region_width]
        right_frame = gray_frame[:, -region_width:]

        keypoints_left, descriptors_left = orb.detectAndCompute(left_frame, None)
        keypoints_right, descriptors_right = orb.detectAndCompute(right_frame, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        current_box = None

        if descriptors_left is not None and descriptors_template is not None:
            matches_left = bf.match(descriptors_template, descriptors_left)
            matches_left = sorted(matches_left, key=lambda x: x.distance)

            if len(matches_left) > MIN_MATCHES:
                print("TikTok watermark detected in the **left** side!")

                pts_left = np.float32([keypoints_left[m.trainIdx].pt for m in matches_left]).reshape(-1, 1, 2)

                if len(pts_left) > 4:
                    x_left, y_left, w_left, h_left = cv2.boundingRect(pts_left)

                    w_left = max(w_left, MIN_WIDTH)
                    h_left = max(h_left, MIN_HEIGHT)

                    x_left = max(0, min(x_left, region_width - MIN_WIDTH))

                    current_box = (x_left, y_left, w_left, h_left)

        if descriptors_right is not None and descriptors_template is not None:
            matches_right = bf.match(descriptors_template, descriptors_right)
            matches_right = sorted(matches_right, key=lambda x: x.distance)

            if len(matches_right) > MIN_MATCHES:
                print("TikTok watermark detected in the **right** side!")

                pts_right = np.float32([keypoints_right[m.trainIdx].pt for m in matches_right]).reshape(-1, 1, 2)

                if len(pts_right) > 4:
                    x_right, y_right, w_right, h_right = cv2.boundingRect(pts_right)

                    w_right = max(w_right, MIN_WIDTH)
                    h_right = max(h_right, MIN_HEIGHT)

                    x_right = frame_width - region_width + x_right  

                    current_box = (x_right, y_right, w_right, h_right)

        if current_box is not None:
            prev_box = current_box
            prev_box_found = True
            prev_frame_count = 0  
        else:
            prev_frame_count += 1
            if prev_frame_count > MAX_NO_DETECTION_FRAMES:
                prev_box_found = False  

        if prev_box_found and prev_box is not None:
            x, y, w, h = prev_box
            roi = frame[y:y+h, x:x+w]
            blurred_roi = cv2.GaussianBlur(roi, (99, 99), 30)
            frame[y:y+h, x:x+w] = blurred_roi

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()

    if os.path.exists(output_path):
        os.remove(output_path)
        print(f"Deleted existing final video: {output_path}")

    print(f"Combining {audio_path} and {temp_output_path} into {output_path}.")
    subprocess.run([
        'ffmpeg', '-y', '-i', temp_output_path, '-i', audio_path, 
        '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_path
    ])

    os.remove(audio_path)
    os.remove(temp_output_path)
 
    print(f"Video processing complete. Final video saved at: {output_path}")

    cv2.destroyAllWindows()

    return {"status": "complete"}
