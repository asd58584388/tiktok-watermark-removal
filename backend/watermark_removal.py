import cv2
import numpy as np
import argparse
import time
import os
import onnxruntime

def preprocess_image(img, input_height=640, input_width=640):
    """Preprocess image for the ONNX model"""
    # Resize
    resized = cv2.resize(img, (input_width, input_height))
    
    # Convert to RGB (from BGR)
    rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
    
    # Normalize to [0,1]
    normalized = rgb.astype(np.float32) / 255.0
    
    # Change shape from HWC to CHW format
    chw = normalized.transpose(2, 0, 1)
    
    # Add batch dimension
    batched = np.expand_dims(chw, axis=0)
    
    return batched

def postprocess_output(output, img_shape, input_shape=(640, 640), conf_threshold=0.25):
    """Process ONNX model output to get bounding boxes"""
    # YOLOv7 output format: [batch, num_detections, 7]
    # Where each detection is: [x, y, w, h, box_score, class_score, class_id]
    
    detections = []
    
    # No detections
    if output.shape[1] == 0:
        return detections
    
    # Get scaling factors
    img_height, img_width = img_shape[:2]
    input_height, input_width = input_shape
    x_factor = img_width / input_width
    y_factor = img_height / input_height
    
    # Process detections
    for i in range(output.shape[1]):
        confidence = output[0, i, 4]
        
        if confidence >= conf_threshold:
            # Extract box coordinates
            x = output[0, i, 0]
            y = output[0, i, 1]
            w = output[0, i, 2]
            h = output[0, i, 3]
            
            # Convert to xyxy format
            x1 = x - w/2
            y1 = y - h/2
            x2 = x + w/2
            y2 = y + h/2
            
            # Scale back to original image size
            x1 = int(x1 * x_factor)
            y1 = int(y1 * y_factor)
            x2 = int(x2 * x_factor)
            y2 = int(y2 * y_factor)
            
            # Store detection
            detections.append({
                'xmin': x1, 
                'ymin': y1, 
                'xmax': x2, 
                'ymax': y2,
                'confidence': float(confidence)
            })
    
    return detections

def detect_watermark(video_path, model_path="yolov7_tiktok_watermark.onnx", conf_threshold=0.25):
    """
    Detect watermarks from an MP4 video using the ONNX model.
    Samples 20 frames and checks for watermarks.
    Returns True if watermark is detected in majority of frames, False otherwise.
    """

    print(f"Detecting watermarks in {video_path}...")
    # Check if model exists
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(__file__), "yolov7_tiktok_watermark.onnx")
        if not os.path.exists(model_path):
            print(f"Error: Model file {model_path} not found")
            return False
    
    # Load ONNX model
    session = onnxruntime.InferenceSession(model_path)
    
    # Open video file
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return False
    
    # Get video properties
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Determine sampling interval to get approximately 20 frames
    sample_count = min(20, frame_count)
    interval = max(1, frame_count // sample_count)
    
    # Track watermark detections
    watermark_detected_count = 0
    frames_processed = 0
    
    for i in range(0, frame_count, interval):
        # Set frame position
        cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ret, frame = cap.read()
        
        if not ret:
            continue
        
        # Preprocess frame
        input_tensor = preprocess_image(frame)
        
        # Run inference
        outputs = session.run(['output'], {'input': input_tensor})
        output = outputs[0]
        
        # Process output to get detections
        detections = postprocess_output(output, frame.shape, conf_threshold=conf_threshold)
        
        # Count frames with watermarks
        if len(detections) > 0:
            watermark_detected_count += 1
        
        frames_processed += 1
        
        # Early exit if we've already processed enough frames with watermarks
        if watermark_detected_count > frames_processed / 2 and frames_processed >= sample_count / 2:
            cap.release()
            return True
    
    cap.release()
    

    print(watermark_detected_count, frames_processed)

    # Return True if watermarks were detected in more than 50% of sampled frames
    return watermark_detected_count > frames_processed / 2

def remove_watermark(frame, model_path="yolov7_tiktok_watermark.onnx", conf_threshold=0.25):
    """Remove watermarks from an image using the ONNX model"""
    # Start timer
    start = time.time()
    
    # Check if model exists
    if not os.path.exists(model_path):
        model_path = os.path.join(os.path.dirname(__file__), "yolov7_tiktok_watermark.onnx")
        if not os.path.exists(model_path):
            print(f"Error: Model file {model_path} not found")
            return False
    
    # Load ONNX model
    # print(f"Loading ONNX model from {model_path}...")
    session = onnxruntime.InferenceSession(model_path)
    
    # Read the image
    # print(f"Reading image from {image_path}...")

    if frame is None:
        print(f"Error: Could not read frame ")
        return False
    
    # Preprocess image
    input_tensor = preprocess_image(frame)
    
    # Run inference
    # print("Detecting watermarks...")
    outputs = session.run(['output'], {'input': input_tensor})
    print(outputs);
    output = outputs[0]
    
    # Process output to get detections
    detections = postprocess_output(output, frame.shape, conf_threshold=conf_threshold)
    
    if not detections:
        # print("No watermarks detected in the image!")
        # cv2.imwrite(output_path, image)
        return frame
    
    # Create a mask for the detected watermarks
    # print("Creating mask for watermarks...")
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    
    # Draw the watermark regions on the mask
    for box in detections:
        x1, y1, x2, y2 = int(box['xmin']), int(box['ymin']), int(box['xmax']), int(box['ymax'])
        # Draw the filled rectangle on the mask
        mask = cv2.rectangle(mask, (x1, y1), (x2, y2), (255, 255, 255), -1)
    
    # Use inpainting to remove the watermark
    # print("Removing watermarks using inpainting...")
    result = cv2.inpaint(frame, mask, 3, cv2.INPAINT_TELEA)
    
    # Save the result
    # print(f"Saving result to {output_path}...")
    # cv2.imwrite(output_path, result)
    
    # End timer
    end = time.time()
    print(f"Time elapsed: {round(end - start, 2)} seconds")
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Remove watermarks from images using YOLOv7 ONNX model")
    parser.add_argument("--image", type=str, required=True, help="Path to the input image")
    parser.add_argument("--output", type=str, required=True, help="Path to save the output image")
    parser.add_argument("--model", type=str, default="yolov7_tiktok_watermark.onnx", help="Path to the ONNX model")
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold for detections")
    args = parser.parse_args()
    
    success = remove_watermark(args.image, args.output, args.model, args.conf)
    
    if success:
        print(f"Watermark removal complete! Check {args.output}")
    else:
        print("Watermark removal failed!")
