from pydantic import BaseModel

class MriMachineAlertDTO(BaseModel):
    issue: str

class InfusionPumpDTO(BaseModel):
    issue: str

class XRayMachineDTO(BaseModel):
    issue: str

class HeartMonitorDTO(BaseModel):
    issue: str