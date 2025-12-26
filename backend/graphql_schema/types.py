"""
Strawberry GraphQL type definitions
These types define the GraphQL schema structure
"""

import strawberry
from typing import Optional, List
from datetime import datetime


@strawberry.type
class Appointment:
    """GraphQL type for Appointment - matches AppointmentResponse from Pydantic"""
    id: str
    patient_name: str
    date: str
    time: str
    duration: int
    doctor_name: str
    status: str
    mode: str
    created_at: str


@strawberry.input
class CreateAppointmentInput:
    """GraphQL input type for creating appointments"""
    patient_name: str
    date: str
    time: str
    duration: int
    doctor_name: str
    mode: str = "In-person"
    status: Optional[str] = "Scheduled"


@strawberry.input
class UpdateAppointmentStatusInput:
    """GraphQL input type for updating appointment status"""
    id: str
    status: str


@strawberry.type
class MutationResponse:
    """Generic response type for mutations"""
    success: bool
    message: str
    appointment: Optional[Appointment] = None
