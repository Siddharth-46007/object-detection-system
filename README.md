
# Object Detection Microservices System

## Overview
This project implements a microservices-based object detection system using YOLOv8 and Flask. It consists of two main components:
- **UI Backend**: Handles image uploads and user requests.
- **AI Backend**: Performs object detection and returns results in JSON format.

## Architecture
- **ui-backend/**: User interface backend service (Flask)
- **ai-backend/**: AI processing service (Flask + YOLOv8)
- **docker-compose.yml**: Container orchestration for both services
- **documentation.md**: Detailed documentation and references

## Prerequisites
- Docker
- Docker Compose

## Setup & Usage
1. **Build and start the services:**
	```bash
	docker-compose up --build
	```
2. **Test object detection:**
	```bash
	curl -X POST -F "image=@test_image.jpg" http://localhost:5000/detect
	```
	- Replace `test_image.jpg` with your image file.
3. **View results:**
	- Detection results are shown in your terminal as JSON.
	- Output images and JSON files are saved in `ai-backend/outputs/`.

## API Endpoints
### UI Backend
- `POST /detect` : Upload image for detection
- `GET /health` : Health check

### AI Backend
- `POST /predict` : Process image and return detections
- `GET /health` : Health check
- `GET /download/<filename>` : Download output files

## Features
- Microservices architecture
- YOLOv8 object detection (CPU-based)
- Docker containerization
- REST API communication
- JSON output with bounding boxes

## Deliverables
- Project folder (zip or GitHub link)
- Documentation with setup steps and references
- Output images (with bounding boxes) and JSON files

## References
- [YOLOv8](https://github.com/ultralytics/ultralytics)
- [YOLOv3](https://github.com/ultralytics/yolov3)
- [Flask](https://flask.palletsprojects.com/)
- [Docker](https://docs.docker.com/)