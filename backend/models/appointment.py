"""
Pydantic models for Appointment data validation.
Aligned with SwasthiQ's clinical data validation requirements.
"""

from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, field_validator, ConfigDict


class AppointmentBase(BaseModel):
    """Base appointment model with shared fields"""
    patient_name: str = Field(
        ..., 
        min_length=2, 
        max_length=100,
        description="Patient's full name"
    )
    date: str = Field(
        ...,
        description="Appointment date in YYYY-MM-DD format"
    )
    time: str = Field(
        ...,
        description="Appointment time in HH:MM format (24-hour)"
    )
    duration: int = Field(
        ...,
        ge=15,  # Minimum 15 minutes
        le=240,  # Maximum 4 hours
        description="Appointment duration in minutes"
    )
    doctor_name: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Doctor's full name"
    )
    mode: Literal["In-person", "Video", "Phone"] = Field(
        default="In-person",
        description="Consultation mode"
    )
    
    @field_validator('date')
    @classmethod
    def validate_date_format(cls, v: str) -> str:
        """Validate date is in correct format"""
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    @field_validator('time')
    @classmethod
    def validate_time_format(cls, v: str) -> str:
        """Validate time is in correct format"""
        try:
            datetime.strptime(v, '%H:%M')
            return v
        except ValueError:
            raise ValueError('Time must be in HH:MM format (24-hour)')


class CreateAppointmentInput(AppointmentBase):
    """Input model for creating appointments"""
    status: Optional[Literal["Scheduled", "Confirmed", "Upcoming"]] = Field(
        default="Scheduled",
        description="Initial appointment status"
    )
    
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "patient_name": "Rajesh Kumar",
                "date": "2025-12-28",
                "time": "09:30",
                "duration": 30,
                "doctor_name": "Dr. Sarah Johnson",
                "mode": "In-person",
                "status": "Scheduled"
            }
        }
    )


class UpdateAppointmentStatusInput(BaseModel):
    """Input model for updating appointment status"""
    status: Literal["Scheduled", "Confirmed", "Upcoming", "Completed", "Cancelled"] = Field(
        ...,
        description="New appointment status"
    )


class AppointmentResponse(AppointmentBase):
    """Response model for appointment with all fields"""
    id: str = Field(
        ...,
        description="Unique appointment identifier"
    )
    status: Literal["Scheduled", "Confirmed", "Upcoming", "Completed", "Cancelled"] = Field(
        ...,
        description="Current appointment status"
    )
    created_at: str = Field(
        ...,
        description="Timestamp when appointment was created"
    )
    
    model_config = ConfigDict(from_attributes=True)


class AppointmentFilters(BaseModel):
    """Filters for querying appointments"""
    date: Optional[str] = Field(
        None,
        description="Filter by specific date (YYYY-MM-DD)"
    )
    status: Optional[str] = Field(
        None,
        description="Filter by status"
    )
    doctor_name: Optional[str] = Field(
        None,
        description="Filter by doctor name"
    )
    
    @field_validator('date')
    @classmethod
    def validate_date_if_present(cls, v: Optional[str]) -> Optional[str]:
        """Validate date format if provided"""
        if v is not None:
            try:
                datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ValueError('Date must be in YYYY-MM-DD format')
        return v
