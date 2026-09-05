import cv2
from ultralytics import YOLO

# Load pre-trained lightweight YOLOv8 model
model = YOLO('yolov8n.pt')

def analyze_crowd_density(image_path, threshold=10):
    results = model(image_path)
    person_count = 0
    
    # Class 0 corresponds to 'person' in COCO dataset
    for r in results:
        for box in r.boxes:
            if int(box.cls[0]) == 0:
                person_count += 1
                
    is_crowded = person_count >= threshold
    return {
        "count": person_count,
        "status": "High Density" if is_crowded else "Normal Density",
        "is_crowded": is_crowded
    }
