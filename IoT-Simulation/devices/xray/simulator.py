import socket
import time
import random
import json
import datetime
import struct
import os
from threading import Thread

class XRaySimulator:
    def __init__(self):
        self.device_id = os.environ.get('DEVICE_ID', 'XRAY_001')
        self.manufacturer = "SimuMed"
        self.model = "X3000-Digital"
        self.server_socket = None
        self.clients = []
        self.exposure_settings = {
            'chest': {'kV': 120, 'mAs': 4},
            'skull': {'kV': 75, 'mAs': 20},
            'abdomen': {'kV': 85, 'mAs': 25},
            'extremities': {'kV': 60, 'mAs': 8}
        }
        
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', 11112))  # DICOM default port
        self.server_socket.listen(5)
        print(f"[{self.device_id}] X-Ray simulator listening on port 11112")
        
        accept_thread = Thread(target=self.accept_connections)
        accept_thread.daemon = True
        accept_thread.start()
        
    def accept_connections(self):
        while True:
            client_socket, addr = self.server_socket.accept()
            print(f"[{self.device_id}] New connection from {addr}")
            self.clients.append(client_socket)
            client_thread = Thread(target=self.handle_client, args=(client_socket,))
            client_thread.daemon = True
            client_thread.start()

    def generate_dicom_header(self, study_type):
        now = datetime.datetime.now()
        header = {
            'SOPClassUID': '1.2.840.10008.5.1.4.1.1.1',
            'SOPInstanceUID': f'1.2.826.0.1.3680043.2.1343.{int(time.time())}',
            'StudyDate': now.strftime('%Y%m%d'),
            'StudyTime': now.strftime('%H%M%S'),
            'PatientID': f'PAT{random.randint(10000, 99999)}',
            'PatientName': f'ANONYMOUS^PATIENT^{random.randint(1, 999)}',
            'StudyDescription': f'{study_type} X-Ray',
            'Modality': 'DX',
            'ManufacturerModelName': self.model,
            'DeviceSerialNumber': self.device_id
        }
        return header

    def generate_exposure_data(self, study_type):
        settings = self.exposure_settings[study_type]
        # Add realistic variations
        actual_kV = settings['kV'] + random.uniform(-2, 2)
        actual_mAs = settings['mAs'] + random.uniform(-0.5, 0.5)
        exposure_time = actual_mAs / (random.uniform(200, 250))  # mA range
        
        return {
            'kV': actual_kV,
            'mAs': actual_mAs,
            'exposure_time': exposure_time,
            'DAP': random.uniform(0.1, 2.0),  # Dose Area Product
            'detector_temp': random.uniform(20, 25),
            'system_status': 'READY',
            'image_quality_indicators': {
                'SNR': random.uniform(45, 55),  # Signal to Noise Ratio
                'CNR': random.uniform(20, 30),  # Contrast to Noise Ratio
                'spatial_resolution': random.uniform(3.5, 4.5)  # lp/mm
            }
        }

    def simulate_xray_procedure(self):
        study_types = list(self.exposure_settings.keys())
        while True:
            study_type = random.choice(study_types)
            
            # Generate DICOM header
            header = self.generate_dicom_header(study_type)
            
            # Generate exposure data
            exposure_data = self.generate_exposure_data(study_type)
            
            # Combine data
            transmission_data = {
                'header': header,
                'exposure_data': exposure_data,
                'timestamp': datetime.datetime.now().isoformat(),
                'device_id': self.device_id,
                'procedure_id': f'PROC{random.randint(1000, 9999)}'
            }
            
            # Transmit to all connected clients
            self.broadcast_data(transmission_data)
            
            # Random interval between procedures
            time.sleep(random.uniform(60, 180))  # 1-3 minutes

    def broadcast_data(self, data):
        message = json.dumps(data).encode('utf-8')
        message_length = struct.pack('!I', len(message))
        
        disconnected_clients = []
        for client in self.clients:
            try:
                client.send(message_length)
                client.send(message)
                print(f"[{self.device_id}] Sent {data['procedure_id']} to client")
            except:
                disconnected_clients.append(client)
                
        # Clean up disconnected clients
        for client in disconnected_clients:
            self.clients.remove(client)

    def run(self):
        self.start_server()
        self.simulate_xray_procedure()

    def handle_client(self, client_socket):
        """Handle individual client connection"""
        try:
            # Send initial device info
            device_info = {
                'device_id': self.device_id,
                'manufacturer': self.manufacturer,
                'model': self.model,
                'connection_time': datetime.datetime.now().isoformat()
            }
            client_socket.send(json.dumps(device_info).encode('utf-8') + b'\r\n')
            
            # Keep connection alive until client disconnects
            while True:
                time.sleep(0.1)  # Prevent CPU hogging
                if client_socket not in self.clients:
                    break
                    
        except (ConnectionResetError, BrokenPipeError):
            if client_socket in self.clients:
                self.clients.remove(client_socket)
        finally:
            try:
                client_socket.close()
            except:
                pass

if __name__ == "__main__":
    simulator = XRaySimulator()
    try:
        simulator.run()
    except KeyboardInterrupt:
        print("\nShutting down X-Ray simulator...")