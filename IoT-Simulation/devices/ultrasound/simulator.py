import socket
import time
import random
from datetime import datetime
import numpy as np
from PIL import Image, ImageDraw
import os
import json

class UltrasoundStation:
    def __init__(self, device_id=None, port=2577):
        if device_id is None:
            device_id = os.environ.get('DEVICE_ID', 'US_001')
        self.device_id = device_id
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(1)
        self.running = True
        print(f"Ultrasound Station {self.device_id} initialized on port {self.port}")

    def generate_ultrasound_data(self):
        # Create simulated ultrasound image data
        width, height = 640, 480
        image = Image.new('L', (width, height), 0)
        draw = ImageDraw.Draw(image)
        
        # Generate random structures
        for _ in range(random.randint(3, 8)):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(20, 100)
            brightness = random.randint(100, 255)
            draw.ellipse([x-size/2, y-size/2, x+size/2, y+size/2], 
                        fill=brightness)
        
        return np.array(image)

    def run(self):
        while self.running:
            try:
                print("Waiting for connection...")
                conn, addr = self.socket.accept()
                print(f"Connected by {addr}")
                
                while True:
                    image_data = self.generate_ultrasound_data()
                    status = {
                        "device_id": self.device_id,
                        "timestamp": datetime.now().isoformat(),
                        "status": "scanning",
                        "probe_type": random.choice(["linear", "curved", "phased"]),
                        "frequency": round(random.uniform(2.0, 15.0), 1),  # MHz
                        "depth": random.randint(5, 30),  # cm
                        "gain": random.randint(50, 100)  # dB
                    }
                    
                    conn.sendall(json.dumps(status).encode() + b'\n')
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    device_id = os.environ.get('DEVICE_ID', 'US_001')
    station = UltrasoundStation(device_id=device_id)
    station.run()