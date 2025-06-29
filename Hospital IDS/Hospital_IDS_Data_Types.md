
# 📁 Hospital IoT IDS - Data Types & Examples

This document lists all data types that the Intrusion Detection System receives, sends, or stores.

---

## 🔌 1. IoT Device Telemetry Data
```json
{
  "device_id": "ecg_001",
  "device_type": "ECG_monitor",
  "timestamp": "2025-06-21T14:15:00Z",
  "metric_name": "heart_rate",
  "value": 78,
  "unit": "bpm",
  "ip_address": "192.168.0.101",
  "mac_address": "AA:BB:CC:DD:EE:FF",
  "firmware_version": "2.0.3",
  "location": "Ward A - Bed 4",
  "status": "active"
}
```

## 🌐 2. Network Traffic Metadata
```json
{
  "source_ip": "192.168.0.101",
  "dest_ip": "192.168.0.200",
  "source_port": 443,
  "dest_port": 135,
  "protocol": "TCP",
  "packet_size": 580,
  "flags": ["SYN", "ACK"],
  "payload_hash": "d9f83a4567eab8f0...",
  "timestamp": "2025-06-21T14:15:03Z",
  "device_id": "infusion_04"
}
```

## 🚨 3. Real-Time Alert
```json
{
  "alert_id": "alert_00045",
  "device_id": "infusion_04",
  "threat_type": "unauthorized_access",
  "severity": "critical",
  "description": "Login attempt from unknown source",
  "suggested_action": "Isolate and investigate device",
  "timestamp": "2025-06-21T14:15:08Z"
}
```

## 🧾 4. Stored Threat Event
```json
{
  "event_id": "event_4523",
  "device_id": "ecg_001",
  "network_trace_id": "trace_203",
  "threat_type": "DoS",
  "detected_by": "ML_model_v2",
  "raw_data": "SGVsbG8gd29ybGQ=",
  "risk_score": 91.4,
  "quarantined": true,
  "actions_taken": ["alerted_admin", "device_quarantined"],
  "timestamp": "2025-06-21T14:15:10Z"
}
```

## 🧠 5. ML Detection Input/Output
**Input:**
```json
{
  "device_id": "ventilator_02",
  "normalized_metrics": [0.42, 0.38, 0.77],
  "time_series_window": [0.40, 0.42, 0.43],
  "device_context": {
    "device_type": "ventilator",
    "firmware_version": "1.2.7"
  }
}
```
**Output:**
```json
{
  "anomaly_score": 0.91,
  "label": "anomaly",
  "confidence": 0.96
}
```

## 📋 6. Device Inventory Metadata
```json
{
  "device_id": "infusion_04",
  "device_type": "infusion_pump",
  "ip_address": "192.168.0.104",
  "mac_address": "00:11:22:33:44:55",
  "location": "Operating Room 2",
  "manufacturer": "BioCare Inc.",
  "registered_on": "2025-05-01T10:00:00Z",
  "last_seen": "2025-06-21T14:15:00Z",
  "firmware_version": "3.2.1",
  "vulnerabilities": ["CVE-2024-11234", "CVE-2023-77890"]
}
```

## 👤 7. User Authentication Data
```json
{
  "user_id": "admin_001",
  "username": "rootadmin",
  "email": "admin@hospital.local",
  "password_hash": "$2b$12$yJW...",
  "roles": ["admin", "security_analyst"],
  "session_token": "eyJhbGciOiJIUzI1...",
  "last_login": "2025-06-21T13:40:00Z"
}
```

## 📜 8. Audit Log Entry
```json
{
  "log_id": "log_8931",
  "event_type": "device_removed",
  "user_id": "admin_001",
  "details": {
    "device_id": "infusion_02",
    "reason": "Decommissioned"
  },
  "timestamp": "2025-06-21T14:00:00Z"
}
```

## ☁️ 9. Cloud Sync Payload
```json
{
  "system_snapshot": {
    "total_devices": 35,
    "connected": 30,
    "alerts_in_progress": 2
  },
  "summary_stats": {
    "alerts_today": 16,
    "devices_quarantined": 3
  },
  "timestamp": "2025-06-21T14:20:00Z"
}
```

## 📊 10. Dashboard Analytics Data
```json
{
  "daily_threats": 12,
  "avg_response_time_minutes": 1.7,
  "top_incident_devices": ["infusion_04", "ecg_001"],
  "uptime": {
    "infusion_04": 99.3,
    "ecg_001": 97.8
  },
  "alerts_by_severity": {
    "low": 3,
    "medium": 6,
    "high": 2,
    "critical": 1
  }
}
```
