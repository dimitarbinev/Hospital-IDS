import socket
import time
import random
from datetime import datetime
import pydicom
from pydicom.dataset import Dataset, FileDataset
import numpy as np
import os
import json

class MRIScanner:
    def __init__(self, device_id=None, port=2576):
        if device_id is None:
            device_id = os.environ.get('DEVICE_ID', 'MRI_001')
        self.device_id = device_id
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(1)
        self.running = True
        print(f"MRI Scanner {self.device_id} initialized on port {self.port}")

    def generate_mri_data(self):
        # Create a basic DICOM dataset
        file_meta = Dataset()
        file_meta.MediaStorageSOPClassUID = '1.2.840.10008.5.1.4.1.1.4'
        file_meta.MediaStorageSOPInstanceUID = '1.2.3'
        file_meta.ImplementationClassUID = '1.2.3.4'

        ds = FileDataset(None, {}, file_meta=file_meta, preamble=b"\0" * 128)
        
        # Add required DICOM tags
        ds.PatientID = f"PAT{random.randint(1000, 9999)}"
        ds.PatientName = "ANONYMOUS"
        ds.StudyDate = datetime.now().strftime('%Y%m%d')
        ds.StudyTime = datetime.now().strftime('%H%M%S')
        ds.Modality = "MR"
        ds.SeriesInstanceUID = f"1.2.3.4.{random.randint(1000, 9999)}"
        
        # Generate random image data
        image_size = 64
        image_data = np.random.randint(0, 4096, size=(image_size, image_size), dtype=np.uint16)
        ds.PixelData = image_data.tobytes()
        
        return ds

    def run(self):
        while self.running:
            try:
                print("Waiting for connection...")
                conn, addr = self.socket.accept()
                print(f"Connected by {addr}")
                
                while True:
                    mri_data = self.generate_mri_data()
                    status = {
                        "device_id": self.device_id,
                        "timestamp": datetime.now().isoformat(),
                        "status": "scanning",
                        "magnet_temp": round(random.uniform(2.5, 4.0), 2),  # Kelvin
                        "helium_level": round(random.uniform(85, 100), 1),  # Percentage
                        "gradient_duty_cycle": round(random.uniform(40, 60), 1)  # Percentage
                    }
                    
                    conn.sendall(json.dumps(status).encode() + b'\n')
                    time.sleep(5)
                    
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    device_id = os.environ.get('DEVICE_ID', 'MRI_001')
    scanner = MRIScanner(device_id=device_id)
    scanner.run()