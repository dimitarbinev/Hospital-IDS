import socket
import time
import random
from datetime import datetime
import os
import json

class InfusionPump:
    def __init__(self, device_id=None, port=2578):
        if device_id is None:
            device_id = os.environ.get('DEVICE_ID', 'INF_001')
        self.device_id = device_id
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Add socket reuse to avoid "Address already in use" errors
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(('0.0.0.0', self.port))
        self.socket.listen(1)
        self.running = True
        self.total_volume = 1000  # mL
        self.current_volume = 1000
        self.flow_rate = 2.0  # mL/hour
        print(f"Infusion Pump {self.device_id} initialized on port {self.port}")

    def update_volumes(self):
        time_delta = 1/3600  # 1 second in hours
        volume_change = self.flow_rate * time_delta
        self.current_volume = max(0, self.current_volume - volume_change)

        # Randomly simulate minor flow rate variations
        self.flow_rate += random.uniform(-0.1, 0.1)
        self.flow_rate = max(0.1, min(self.flow_rate, 10.0))

    def run(self):
        while self.running:
            try:
                print("Waiting for connection...")
                conn, addr = self.socket.accept()
                print(f"Connected by {addr}")

                while True:
                    self.update_volumes()

                    # Add basic alarms
                    alarms = []
                    if self.current_volume <= 100:
                        alarms.append("LOW_VOLUME")
                    if self.current_volume <= 0:
                        alarms.append("EMPTY")

                    status = {
                        "device_id": self.device_id,
                        "timestamp": datetime.now().isoformat(),
                        "status": "running" if self.current_volume > 0 else "empty",
                        "current_volume_ml": round(self.current_volume, 2),
                        "flow_rate_ml_h": round(self.flow_rate, 2),
                        "battery_level": random.randint(0, 100),
                        "occlusion_pressure": round(random.uniform(0, 15), 1),  # PSI
                        "air_in_line": random.random() < 0.01,  # 1% chance of air detection
                        "alarms": alarms
                    }

                    # Send as JSON instead of string representation
                    conn.sendall(json.dumps(status).encode() + b'\n')
                    time.sleep(1)

            except ConnectionResetError:
                print("Client disconnected")
                conn.close()
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    device_id = os.environ.get('DEVICE_ID', 'INF_001')
    pump = InfusionPump(device_id=device_id)
    pump.run()