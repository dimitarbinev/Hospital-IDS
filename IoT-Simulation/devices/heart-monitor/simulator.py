import socket
import time
import random
import json
import datetime
from threading import Thread
from math import sin, cos, pi
import struct
import os

class HeartMonitor:
    def __init__(self, device_id=None):
        if device_id is None:
            device_id = os.environ.get("DEVICE_ID", "HR_001")
        self.device_id = device_id
        self.manufacturer = "SimuMed"
        self.model = "CardioTech-2000"
        self.server_socket = None
        self.clients = []
        self.patient_data = self.initialize_patient_data()
        
    def initialize_patient_data(self):
        return {
            'patient_id': f'PAT{random.randint(10000, 99999)}',
            'age': random.randint(25, 85),
            'weight': random.randint(50, 120),
            'height': random.randint(150, 190),
            'base_heart_rate': random.randint(60, 80)
        }

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(('0.0.0.0', 2575))  # HL7 default port
        self.server_socket.listen(5)
        print(f"[{self.device_id}] Heart monitor simulator listening on port 2575")
        
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

    def generate_vital_signs(self):
        # Generate realistic vital signs with natural variations
        base_hr = self.patient_data['base_heart_rate']
        current_time = time.time()
        
        # Add circadian rhythm variation
        hour = datetime.datetime.now().hour
        circadian_variation = -5 if 0 <= hour <= 4 else 5 if 12 <= hour <= 15 else 0
        
        # Generate heart rate with natural variations
        heart_rate = base_hr + circadian_variation + random.uniform(-3, 3)
        
        # Generate blood pressure with correlation to heart rate
        systolic = 120 + (heart_rate - 70) * 0.5 + random.uniform(-5, 5)
        diastolic = 80 + (heart_rate - 70) * 0.3 + random.uniform(-3, 3)
        
        # Generate oxygen saturation
        spo2 = random.uniform(95, 100)
        
        # Generate temperature with slight variations
        temperature = 36.8 + random.uniform(-0.2, 0.2)
        
        # Generate respiratory rate correlated with heart rate
        respiratory_rate = (heart_rate / 4) + random.uniform(-1, 1)
        
        return {
            'timestamp': datetime.datetime.now().isoformat(),
            'heart_rate': round(heart_rate, 1),
            'blood_pressure': {
                'systolic': round(systolic, 1),
                'diastolic': round(diastolic, 1)
            },
            'spo2': round(spo2, 1),
            'temperature': round(temperature, 1),
            'respiratory_rate': round(respiratory_rate, 1),
            'ecg_data': self.generate_ecg_data(heart_rate),
            'device_status': {
                'battery_level': random.uniform(60, 100),
                'signal_quality': random.uniform(0.8, 1.0),
                'leads_status': 'CONNECTED',
                'alarm_status': self.check_alarm_conditions(heart_rate, spo2, systolic, diastolic)
            }
        }

    def generate_ecg_data(self, heart_rate):
        # Simplified ECG wave generation
        samples = []
        interval = 60 / heart_rate  # seconds between beats
        sample_rate = 250  # Hz
        points_per_beat = int(interval * sample_rate)
        
        # Generate one beat of ECG data
        for i in range(points_per_beat):
            t = i / sample_rate
            # Simplified ECG wave shape
            if t < 0.1:  # P wave
                value = 0.25 * (1 - cos(2 * pi * t / 0.1))
            elif t < 0.2:  # QRS complex
                value = sin(2 * pi * t / 0.1)
            elif t < 0.4:  # T wave
                value = 0.3 * (1 - cos(2 * pi * (t - 0.2) / 0.2))
            else:
                value = 0
                
            # Add some noise
            value += random.uniform(-0.05, 0.05)
            samples.append(round(value, 3))
            
        return samples

    def check_alarm_conditions(self, hr, spo2, systolic, diastolic):
        alarms = []
        
        if hr > 100:
            alarms.append('TACHYCARDIA')
        elif hr < 60:
            alarms.append('BRADYCARDIA')
            
        if spo2 < 90:
            alarms.append('LOW_SPO2')
            
        if systolic > 180 or diastolic > 110:
            alarms.append('HYPERTENSION')
        elif systolic < 90 or diastolic < 60:
            alarms.append('HYPOTENSION')
            
        return alarms if alarms else 'NORMAL'

    def broadcast_data(self, data):
        message = json.dumps(data).encode('utf-8') + b'\r\n'
        disconnected_clients = []
        
        for client in self.clients:
            try:
                client.send(message)
            except:
                disconnected_clients.append(client)
                
        # Clean up disconnected clients
        for client in disconnected_clients:
            self.clients.remove(client)

    def simulate_monitoring(self):
        while True:
            vital_signs = self.generate_vital_signs()
            
            # Prepare HL7 message
            transmission_data = {
                'device_id': self.device_id,
                'patient_data': self.patient_data,
                'vital_signs': vital_signs,
                'message_type': 'ORU^R01',
                'message_id': f'MSG{int(time.time())}'
            }
            
            self.broadcast_data(transmission_data)
            
            # Send updates every second
            time.sleep(1)

    def run(self):
        self.start_server()
        self.simulate_monitoring()

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
            message = json.dumps(device_info).encode('utf-8')
            message_length = struct.pack('!I', len(message))
            client_socket.send(message_length)
            client_socket.send(message)
            
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
    device_id = os.environ.get("DEVICE_ID", "HR_001")
    simulator = HeartMonitor(device_id)
    try:
        simulator.run()
    except KeyboardInterrupt:
        print("\nShutting down heart monitor simulator...")
