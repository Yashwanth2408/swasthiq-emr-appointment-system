"""
GraphQL Query Resolvers
These functions handle data retrieval operations
"""

import strawberry
from typing import List, Optional
from graphql_schema.types import Appointment
from services import appointment_service


@strawberry.type
class Query:
    """Root Query type - all read operations"""
    
    @strawberry.field
    def appointments(
        self,
        date: Optional[str] = None,
        status: Optional[str] = None,
        doctor_name: Optional[str] = None
    ) -> List[Appointment]:
        """
        Query appointments with optional filters
        
        Args:
            date: Filter by appointment date (YYYY-MM-DD)
            status: Filter by appointment status
            doctor_name: Filter by doctor's name
        
        Returns:
            List of appointments matching filters
        
        Example Query:
            query {
              appointments(date: "2025-12-27", status: "Confirmed") {
                id
                patientName
                doctorName
                time
                status
              }
            }
        """
        # Call service layer
        appointments = appointment_service.get_appointments(
            date=date,
            status=status,
            doctor_name=doctor_name
        )
        
        # Convert Pydantic models to Strawberry types
        return [
            Appointment(
                id=apt.id,
                patient_name=apt.patient_name,
                date=apt.date,
                time=apt.time,
                duration=apt.duration,
                doctor_name=apt.doctor_name,
                status=apt.status,
                mode=apt.mode,
                created_at=apt.created_at
            )
            for apt in appointments
        ]
    
    @strawberry.field
    def appointment(self, id: str) -> Optional[Appointment]:
        """
        Get a single appointment by ID
        
        Args:
            id: Appointment identifier
        
        Returns:
            Appointment object or None if not found
        """
        appointments = appointment_service.get_appointments()
        
        for apt in appointments:
            if apt.id == id:
                return Appointment(
                    id=apt.id,
                    patient_name=apt.patient_name,
                    date=apt.date,
                    time=apt.time,
                    duration=apt.duration,
                    doctor_name=apt.doctor_name,
                    status=apt.status,
                    mode=apt.mode,
                    created_at=apt.created_at
                )
        
        return None
