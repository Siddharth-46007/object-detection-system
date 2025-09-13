import requests

def test_detection():
    # Download a test image
    img_url = "https://images.unsplash.com/photo-1518717758536-85ae29035b6d?w=400"
    img_response = requests.get(img_url)
    
    if img_response.status_code == 200:
        # Save image temporarily
        with open('test_image.jpg', 'wb') as f:
            f.write(img_response.content)
        
        # Test detection API
        url = 'https://potential-space-carnival-jvgjv4jgj95fqr7p-5000.app.github.dev/detect'
        
        with open('test_image.jpg', 'rb') as f:
            files = {'image': f}
            response = requests.post(url, files=files)
        
        print("Response:", response.status_code)
        print("Result:", response.json())
    else:
        print("Failed to download test image")

if __name__ == '__main__':
    test_detection()