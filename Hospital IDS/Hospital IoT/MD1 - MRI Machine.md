# ==MRI Machine Simulation==

The Magnetic Resonance Imaging (MRI) machine is represented in the project as a lightweight Linux-based distribution called [[Alpine Linux]]. This distribution was chosen because it is lightweight and allows us to simulate how an MRI device could be exploited for security breaches in an Internet of Things (IoT) hospital environment, potentially exposing sensitive information about patients and workers.

## Alpine Setup
- The Alpine Linux system runs on [[Oracle VirtualBox]] — a hardware virtualization platform that simulates computers in a software environment.
- This setup makes it possible to manage the device entirely in one place without needing dedicated physical hardware.

## Data Transit
- Mock data is transmitted from the Alpine Virtual Machine to the Ubuntu-based server.  
- A pre-built Python script runs automatically every time the Virtual Machine powers on, ensuring persistence similar to a real medical device.

## Network
- The data is transmitted over an internal network dedicated to medical devices and the Ubuntu-based server.  
- Additionally, the Virtual Machine has a secondary adapter connected to Wireless Fidelity (Wi-Fi) for communication with external computers during development.  
- This second adapter is temporary and will be removed after development is complete.

## Data Representation
