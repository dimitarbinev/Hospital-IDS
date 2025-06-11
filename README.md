
# 🏥 Healthcare IoT Intrusion Detection & Response System

## 📌 Project Overview
**Goal:** Simulate a hospital network (IoT + traditional devices) and detect intrusions via rule-based + ML-based IDS, with real-time alerting, logging, REST API, and dashboard.

---

## 🧱 Project Structure

```plaintext
project-root/
├── devices/                     # Simulated devices (Python or GNS3 nodes)
├── ids/                         # IDS engine, rules, ML
├── backend/                     # FastAPI app (REST + WebSocket)
├── dashboard/                   # React or Flask frontend
├── database/                    # Schema, DB connectors
├── cloud/                       # Alert integrations (Discord, Email)
├── config/                      # JSON device configs & alert settings
├── scripts/                     # Bash utilities, launchers
├── logs/                        # Alert logs and history
└── README.md
```

---

## 🚀 Technologies Used

### 🧪 Device Simulation
- GNS3 (with Linux/Windows VMs)
- TinyCore / Alpine Linux
- `socket`, `asyncio` (Python)
- Traffic tools: `netcat`, `nmap`, `hping3`

### 🛡 IDS Engine
- `Scapy` / `PyShark`
- `socket` / `asyncio`
- Custom rule logic
- Packet parsing + behavior modeling

### 🤖 Machine Learning
- `scikit-learn` or `PyOD`
- Isolation Forest / One-Class SVM
- `numpy`, `pandas` for preprocessing
- Custom training data based on traffic

### 🌐 Backend (FastAPI)
- FastAPI (REST + WebSocket)
- `pydantic` for models
- `uvicorn` for serving
- REST routes for:
  - `/alerts`, `/alerts/{device_id}`
  - `/devices`, `/status`
  - WebSocket: `/ws`

### 💾 Database
- MongoDB (`pymongo`, `motor`)
- (or PostgreSQL + `asyncpg`)
- Store: alerts, devices, logs, metrics

### 📊 Dashboard (Frontend)
- React.js (or Flask + JS)
- `WebSocket` client
- `Chart.js` or `Recharts`
- Tailwind CSS or Chakra UI (optional)

### ☁️ Cloud Alerts
- Discord Webhooks
- Email via SMTP or Mailgun
- Telegram Bot API

---

## 📚 What You Need to Learn

### GNS3 & Networking
- Build topologies, TAP interfaces
- Routing traffic to IDS
- Lightweight OSs (TinyCore, Alpine)
- NAT, bridged adapters

### Python IDS
- Packet sniffing (`Scapy`, `PyShark`)
- TCP/IP, UDP, ICMP, HTTP headers
- Custom rule detection logic
- Logging + JSON alert formatting

### ML Detection
- Traffic feature extraction
- Training + testing anomaly models
- `scikit-learn`: IsolationForest, OneClassSVM
- Evaluate false positives / precision

### FastAPI Backend
- Routing, query/POST handling
- WebSocket broadcast
- REST API security (optional)
- Database integration (Mongo or Postgres)

### Dashboard (React)
- WebSocket state updates
- Filtering + sorting data
- Real-time UI updates
- Graphs with `Chart.js`

### Cloud Integration
- How to send POST to Discord webhook
- Use `smtplib` or email API
- Format Telegram messages via Bot API

---

## ✅ Tasks & Planning

### 🔨 Core Features Checklist
- [ ] GNS3 devices: IoT + desktops
- [ ] Packet sniffer engine
- [ ] Detection rules
- [ ] ML model + trainer
- [ ] Alert logging to DB
- [ ] FastAPI backend w/ REST + WS
- [ ] Live dashboard (alerts, devices)
- [ ] Alert history + graphs
- [ ] Discord/Email/Telegram alerting

### 🧠 Advanced / Future
- [ ] Quarantine infected device (iptables sim)
- [ ] CVE lookup for known device types
- [ ] Retraining of ML model weekly
- [ ] User login panel for dashboard
- [ ] Export CSV or PDF logs

---

## 🗂 Notes
- IDS can run **on host** while devices run in **GNS3**
- ML component can run **in parallel** to rules engine
- All alerts use a standard schema:
  ```json
  {
    "device_id": "HRM-01",
    "timestamp": "2025-06-11T12:34:56",
    "alert_type": "anomaly",
    "description": "External IP contact",
    "severity": "high"
  }
  ```

---

## 📍 Important Links
- [GNS3 Download](https://www.gns3.com/software/download)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Scapy Docs](https://scapy.readthedocs.io/)
- [PyShark Docs](https://github.com/KimiNewt/pyshark)
- [scikit-learn Anomaly Detection](https://scikit-learn.org/stable/modules/outlier_detection.html)
