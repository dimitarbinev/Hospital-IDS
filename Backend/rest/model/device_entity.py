from Backend.rest.model.database import Base

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy import Index


class MriMachine(Base):
    __tablename__ = "mri_machine"
    __table_args__ = (Index("ix_mri_device_time", "id", "timestamp"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(String(15), nullable=False)
    patient_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    study_id = Column(String(32), nullable=False)
    status = Column(String(20), nullable=False)
    sequence = Column(String(32), nullable=False)
    progress_percent = Column(Integer, nullable=False)
    current_slice = Column(Integer, nullable=False)
    total_slices = Column(Integer, nullable=False)
    nonce = Column(String(255), nullable=False)
    hmac_sha256 = Column(String(255), nullable=False)

    mri_machine_alerts = relationship("MriMachineAlert", back_populates="mri_machine", cascade="all, delete-orphan")

class InfusionPump(Base):
    __tablename__ = "infusion_pump"
    __table_args__ = (Index("ix_infusion_pump_device_time", "id", "timestamp"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(String(15), nullable=False)
    patient_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    drug = Column(String(64), nullable=False)
    infusion_rate = Column(Integer, nullable=False)
    volume_infused = Column(Integer, nullable=False)
    volume_remaining = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    nonce = Column(String(255), nullable=False)
    hmac_sha256 = Column(String(255), nullable=False)

    infusion_pump_alerts = relationship("InfusionPumpAlert", back_populates="infusion_pump", cascade="all, delete-orphan")

class XRayMachine(Base):
    __tablename__ = "xray_machine"
    __table_args__ = (Index("ix_xray_device_time", "id", "timestamp"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(String(15), nullable=False)
    patient_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    status = Column(String(32), nullable=False)
    tube_temp_C = Column(Integer, nullable=False)
    study_id = Column(String(64), nullable=False)
    image_count = Column(Integer, nullable=False)
    radiation_dose = Column(Integer, nullable=False)
    exam_status = Column(String(32), nullable=False)
    nonce = Column(String(255), nullable=False)
    hmac_sha256 = Column(String(255), nullable=False)

    xray_machine_alerts = relationship("XRayMachineAlert", back_populates="xray_machine", cascade="all, delete-orphan")

class HeartMonitor(Base):
    __tablename__ = "heart_monitor"
    __table_args__ = (Index("ix_heart_monitor_device_time", "id", "timestamp"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(String(15), nullable=False)
    patient_id = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    heart_rate = Column(Integer, nullable=False)
    spo2 = Column(Integer, nullable=False)
    spo2_unit = Column(String(5), nullable=True)
    respiratory_rate = Column(Integer, nullable=False)
    respiratory_rate_unit = Column(String(5), nullable=True)
    battery_pct = Column(Integer, nullable=False)
    nonce = Column(String(255), nullable=False)
    hmac_sha256 = Column(String(255), nullable=False)

    heart_monitor_alerts = relationship("HeartMonitorAlert", back_populates="heart_monitor", cascade="all, delete-orphan")