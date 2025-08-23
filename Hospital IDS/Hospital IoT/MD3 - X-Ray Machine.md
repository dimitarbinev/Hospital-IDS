# X-Ray Machine Simulation

The X-Ray Machine is represented in the project as a lightweight Linux-based distribution called [[Alpine Linux]]. This simulation showcases how radiology equipment could be targeted as part of broader cybersecurity threats in an Internet of Things (IoT) hospital system.

## Alpine Setup
- The Alpine Linux system is deployed on [[Oracle VirtualBox]], a hardware virtualization platform that allows simulation of entire operating systems.  
- The lightweight nature of Alpine Linux makes it ideal for simulating medical devices in a controlled environment.

## Data Transit
- Mock radiology data is sent from the Alpine Virtual Machine to the Ubuntu-based server.  
- A Python script runs automatically on startup, simulating persistent device communication.

## Network
- The device communicates over an isolated internal hospital network that links only medical devices and the server.  
- A secondary Wireless Fidelity (Wi-Fi) adapter is enabled temporarily for development purposes.

## Data Representation
