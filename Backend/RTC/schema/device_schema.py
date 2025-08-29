from pydantic import BaseModel

class MriMachineDTO(BaseModel):
    device_id: str
    patient_id: int
    study_id: str
    status: str
    sequence: str
    progress_percent: int
    current_slice: int
    total_slices: int
    nonce: str
    hmac_sha256: str

class InfusionPumpDTO(BaseModel):
    device_id: str
    patient_id: int
    drug: str
    infusion_rate: int
    infusion_rate_unit: str
    volume_infused: int
    volume_remaining: int
    status: str
    nonce: str
    hmac_sha256: str

class XRayMachineDTO(BaseModel):
    device_id: str
    patient_id: int
    status: str
    tube_temp_C: int
    study_id: str
    image_count: int
    radiation_dose: int
    radiation_dose_unit: str
    exam_status: str
    nonce: str
    hmac_sha256: str

class HeartMonitorDTO(BaseModel):
    device_id: str
    patient_id: int
    heart_rate: int
    heart_rate_unit: str
    spo2: int
    spo2_unit: str
    respiratory_rate: int
    respiratory_rate_unit: str
    battery_pct: int
    nonce: str
    hmac_sha256: str