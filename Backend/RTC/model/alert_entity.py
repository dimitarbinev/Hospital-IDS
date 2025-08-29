from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from rest.model.database import Base
from sqlalchemy import Index, func


class MriMachineAlert(Base):
    __tablename__ = "mri_alerts_alerts"
    __table_args__ = (Index("ix_mri_alerts_device_id_time", "device_id", "issued_at"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("mri_machine.id", ondelete="CASCADE"), nullable=False)
    issue = Column(String(255), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    status = Column(String(20), nullable=False, default="unresolved")

    mri_machine = relationship("MriMachine", back_populates="mri_machine_alerts")

class InfusionPumpAlert(Base):
    __tablename__ = "infusion_pump_alerts"
    __table_args__ = (Index("ix_infusion_pump_alerts_device_id_time", "device_id", "issued_at"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("infusion_pump.id", ondelete="CASCADE"), nullable=False)
    issue = Column(String(255), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    status = Column(String(20), nullable=False, default="unresolved")

    infusion_pump = relationship("InfusionPump", back_populates="infusion_pump_alerts")

class XRayMachineAlert(Base):
    __tablename__ = "xray_machine_alerts"
    __table_args__ = (Index("ix_xray_alerts_device_id_time", "device_id", "issued_at"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("xray_machine.id", ondelete="CASCADE"), nullable=False)
    issue = Column(String(255), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    status = Column(String(20), nullable=False, default="unresolved")

    xray_machine = relationship("XRayMachine", back_populates="xray_machine_alerts")

class HeartMonitorAlert(Base):
    __tablename__ = "heart_monitor_alerts"
    __table_args__ = (Index("ix_heart_monitor_alerts_device_id_time", "device_id", "issued_at"),)

    id = Column(Integer, primary_key=True)
    device_id = Column(Integer, ForeignKey("heart_monitor.id", ondelete="CASCADE"), nullable=False)
    issue = Column(String(255), nullable=False)
    issued_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    status = Column(String(20), nullable=False, default="unresolved")

    heart_monitor = relationship("HeartMonitor", back_populates="heart_monitor_alerts")