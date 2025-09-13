# Object Detection Microservices Documentation

## Overview
This project implements a microservices-based object detection system using YOLOv8 and Flask.

## Architecture
- **UI Backend (Port 5000)**: Handles file uploads and user requests
- **AI Backend (Port 5001)**: Performs object detection using YOLOv8
- **Communication**: REST API calls between services
- **Containerization**: Docker containers with docker-compose

## References
- YOLOv8: https://github.com/ultralytics/ultralytics
- Flask Documentation: https://flask.palletsprojects.com/
- Docker Documentation: https://docs.docker.com/
- YOLOv3 Reference: https://github.com/ultralytics/yolov3

## API Endpoints

### UI Backend
- `GET /health` - Health check
- `POST /detect` - Upload image for detection

### AI Backend  
- `GET /health` - Health check
- `POST /predict` - Process image and return detections
- `GET /download/<filename>` - Serve output files

## Setup Instructions
1. Clone repository
2. Run `docker-compose up --build`
3. Access UI backend at http://localhost:5000
4. Access AI backend at http://localhost:5001

## Testing
Upload an image via POST request to `/detect` endpoint and receive JSON response with detections and annotated image.