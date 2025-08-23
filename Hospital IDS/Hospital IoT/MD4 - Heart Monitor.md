# Heart Monitor Simulation

The Heart Monitor is represented in the project as a lightweight Linux-based distribution called [[Alpine Linux]]. This simulation highlights how patient-monitoring equipment could be exploited within an Internet of Things (IoT) hospital setting.

## Alpine Setup
- The Heart Monitor runs as an Alpine Linux system inside [[Oracle VirtualBox]].  
- This setup ensures lightweight operation and allows for flexible testing of medical devices.

## Data Transit
- Mock monitoring data is transmitted from the Alpine Virtual Machine to the Ubuntu-based server.  
- A Python script is executed automatically whenever the Virtual Machine starts, ensuring persistent data transfer like a real heart monitor.

## Network
- Communication is handled through an isolated internal hospital network for medical devices and the server.  
- A secondary Wireless Fidelity (Wi-Fi) adapter is enabled during development but removed in secure production environments.

## Data Representation
