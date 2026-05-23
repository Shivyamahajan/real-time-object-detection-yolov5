import os 
import cv2 
import torch 
from torchvision import transforms 
from torch import hub 
 
# Redirect standard output to suppress messages 
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' # Suppress TensorFlow messages 
torch.backends.cudnn.benchmark = True # Speed up GPU computations 
cv2.setNumThreads(0) # OpenCV: Use all available threads for 
processing 
 
# Load YOLOv5 model 
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True) 
model.eval() 
 
# List of objects that the model can accurately detect 
objects_to_detect = [ 
'person', 'bicycle', 'car', 'motorcycle', 'airplane', 'bus', 'train', 'truck', 
'boat', 'traffic light', 'fire hydrant', 'stop sign', 'parking meter', 'bench', 
'bird', 'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear', 'zebra', 
'giraffe', 'backpack', 'umbrella', 'handbag', 'tie', 'suitcase', 'frisbee', 
'skis', 'snowboard', 'sports ball', 'kite', 'baseball bat', 'baseball glove', 
'skateboard', 'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup', 
'fork', 
'knife', 'spoon', 'bowl', 'banana', 'apple', 'sandwich', 'orange', 'broccoli', 
'carrot', 'hot dog', 'pizza', 'donut', 'cake', 'chair', 'couch', 'potted 
plant', 
'bed', 'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote', 'keyboard', 
'cell phone', 'microwave', 'oven', 'toaster', 'sink', 'refrigerator', 'book', 
'clock', 'vase', 'scissors', 'teddy bear', 'hair drier', 'toothbrush', 
'phone', 'fingers', 'keys', 'wallet', 'glasses', 'watch', 'mirror', 'pen', 
'notebook', 'paper', 'shoes', 'socks', 'ring', 'bracelet', 'earrings', 
'necklace', 'belt', 'hat', 'scarf', 'gloves', 'umbrella', 'bag', 'wallet', 
'flashlight', 'towel', 'pillow' 
] 
 
# Define a function to perform real-time object detection 
def detect_objects(): 
27  
# Open camera 
cap = cv2.VideoCapture(0) 
 
while True: 
# Read frame from camera 
ret, frame = cap.read() 
 
# Error handling for None frames 
if frame is None: 
print("Error: Unable to read frame from camera.") 
continue 
 
# Perform object detection 
results = model(frame) 
 
# Parse results 
for detection in results.xyxy[0]: 
conf = float(detection[4]) 
label = int(detection[5]) 
label_name = model.names[label] 
 
# Filter detections by confidence threshold and objects to detect 
if conf > 0.5 and label_name in objects_to_detect: 
x1, y1, x2, y2 = map(int, detection[:4]) 
 
# Draw bounding box and label on the frame 
cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2) 
cv2.putText(frame, label_name, (x1, y1 - 10), 
cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2) 
 
# Display the frame 
cv2.imshow('Real-time Object Detection', frame) 
 
# Exit loop if 'A' key is pressed 
if cv2.waitKey(1) & 0xFF == ord('a'): # Check for 'A' key press 
break 
 
# Release the camera and close all OpenCV windows 
cap.release() 
cv2.destroyAllWindows() 
 
# Run real-time object detection 
detect_objects() 