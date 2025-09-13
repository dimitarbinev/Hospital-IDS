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

| Type            | Value                                                            |
| --------------- | ---------------------------------------------------------------- |
| deviceId        | MRI_001                                                          |
| patientId       | 12345                                                            |
| timestamp       | 2025-08-23T20:45:19.665Z                                         |
| studyId         | STUDY-8a7f12b4                                                   |
| status          | scanning                                                         |
| sequence        | T1-weighted                                                      |
| progressPercent | 38                                                               |
| currentSlice    | 48                                                               |
| totalSlices     | 128                                                              |
| nonce           | 18f3b8246c4e4650a5c7bc9189e5a437                                 |
| hmac_sha256     | ad8cf1e9363b0a38e2a92d314c8e8d6a3cb96b0a5f5cfba9dfe4979e5a3cfa09 |
