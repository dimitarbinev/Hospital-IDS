# ==X-Ray Machine Simulation==

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

| Type              | Value                                                            |
| ----------------- | ---------------------------------------------------------------- |
| deviceId          | XRay_2                                                           |
| patientId         | 24680                                                            |
| timestamp         | 2025-08-23T20:45:15.204Z                                         |
| status            | cooldown                                                         |
| tubeTempC         | 41.7                                                             |
| studyId           | XR-20250823-fc9a12                                               |
| imageCount        | 2                                                                |
| radiationDose     | 1.4                                                              |
| radiationDoseUnit | mGy                                                              |
| examStatus        | completed                                                        |
| nonce             | c6ab0c57f15841f6b0c780f153771890                                 |
| hmac_sha256       | 9f72a3b59b76f36c8b6f5b529ed682e6f523c199bc1d91e0d6763dfc8295fd58 |
