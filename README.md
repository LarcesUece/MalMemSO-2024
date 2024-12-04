# malware-detection

A complete tool for malware detection and containment.

## repository structure

This repository contains three distinct projects, organized into separate folders, that together form the complete malware detection system. Each project is designed to run in a specific environment:

### device/

This folder contains the code that runs on end devices. It is responsible for extracting memory dumps, compressing them, and sending them to the Fog layer. If malware is detected, the device will handle the situation locally.

- Purpose: Memory dump extraction, compression, and malware remediation.
- Environment: Windows 10.
- Technologies: Python.

### fog/

This folder contains the code for the intermediate layer, which analyzes the memory dumps received from devices and classifies them using a pre-trained model provided by the Cloud layer. The classification result determines whether malware is present.

- Purpose: Data analysis, classification, and forwarding results to the devices.
- Environment:
- Technologies: Flask

### cloud/

This folder contains the cloud-level project, which trains and updates the machine learning model used for malware detection. The trained model is then sent to the Fog layer for real-time analysis and classification.

- Purpose: Model training, storage, and distribution to the Fog layer.
- Environment:
- Technologies:
