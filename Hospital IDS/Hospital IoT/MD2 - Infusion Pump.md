# Infusion Pump Simulation

The Infusion Pump is represented in the project as a lightweight Linux-based distribution called [[Alpine Linux]]. The purpose of this simulation is to demonstrate how an infusion device could be used as an entry point in an Internet of Things (IoT) hospital network, potentially exposing sensitive patient and staff information.

## Alpine Setup
- The Alpine Linux system runs on [[Oracle VirtualBox]], which provides hardware virtualization for creating and managing Virtual Machines.  
- This enables lightweight and portable testing of medical IoT devices.

## Data Transit
- Mock infusion data is transmitted from the Alpine Virtual Machine to the Ubuntu-based server.  
- A pre-built Python script runs automatically on startup, ensuring the behavior remains persistent like a real infusion pump.

## Network
- Communication takes place over an internal network between medical devices and the Ubuntu-based server.  
- A secondary Wireless Fidelity (Wi-Fi) adapter provides temporary external connectivity during development and is disabled in production.

## Data Representation
