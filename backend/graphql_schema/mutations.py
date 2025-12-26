"""
GraphQL Mutation Resolvers
These functions handle data modification operations (Create, Update, Delete)
"""

import strawberry
from typing import Optional
from graphql_schema.types import Appointment, CreateAppointmentInput, UpdateAppointmentStatusInput, MutationResponse
from services import appointment_service
from models.appointment import CreateAppointmentInput as PydanticCreateInput


@strawberry.type
class Mutation:
    """Root Mutation type - all write operations"""
    
    @strawberry.mutation
    def create_appointment(self, input: CreateAppointmentInput) -> Appointment:
        """
        Create a new appointment with conflict detection
        
        Args:
            input: Appointment data (patient_name, date, time, duration, doctor_name, mode)
        
        Returns:
            Created appointment object
        
        Raises:
            GraphQL error if validation fails or time conflict detected
        
        Example Mutation:
            mutation {
              createAppointment(input: {
                patientName: "John Doe"
                date: "2025-12-28"
                time: "10:00"
                duration: 30
                doctorName: "Dr. Sarah Johnson"
                mode: "In-person"
              }) {
                id
                patientName
                status
                createdAt
              }
            }
        """
        # Convert Strawberry input to Pydantic model for validation
        pydantic_input = PydanticCreateInput(
            patient_name=input.patient_name,
            date=input.date,
            time=input.time,
            duration=input.duration,
            doctor_name=input.doctor_name,
            mode=input.mode,
            status=input.status
        )
        
        # Call service layer (will raise ValueError if conflict)
        created_appointment = appointment_service.create_appointment(pydantic_input)
        
        # Convert response to Strawberry type
        return Appointment(
            id=created_appointment.id,
            patient_name=created_appointment.patient_name,
            date=created_appointment.date,
            time=created_appointment.time,
            duration=created_appointment.duration,
            doctor_name=created_appointment.doctor_name,
            status=created_appointment.status,
            mode=created_appointment.mode,
            created_at=created_appointment.created_at
        )
    
    @strawberry.mutation
    def update_appointment_status(self, id: str, status: str) -> Appointment:
        """
        Update appointment status
        
        Args:
            id: Appointment identifier
            status: New status (Scheduled, Confirmed, Upcoming, Completed, Cancelled)
        
        Returns:
            Updated appointment object
        
        Example Mutation:
            mutation {
              updateAppointmentStatus(id: "apt-001", status: "Confirmed") {
                id
                status
              }
            }
        """
        updated_appointment = appointment_service.update_appointment_status(id, status)
        
        return Appointment(
            id=updated_appointment.id,
            patient_name=updated_appointment.patient_name,
            date=updated_appointment.date,
            time=updated_appointment.time,
            duration=updated_appointment.duration,
            doctor_name=updated_appointment.doctor_name,
            status=updated_appointment.status,
            mode=updated_appointment.mode,
            created_at=updated_appointment.created_at
        )
    
    @strawberry.mutation
    def delete_appointment(self, id: str) -> MutationResponse:
        """
        Delete an appointment
        
        Args:
            id: Appointment identifier
        
        Returns:
            Success response with message
        
        Example Mutation:
            mutation {
              deleteAppointment(id: "apt-001") {
                success
                message
              }
            }
        """
        try:
            success = appointment_service.delete_appointment(id)
            return MutationResponse(
                success=success,
                message=f"Appointment {id} deleted successfully"
            )
        except ValueError as e:
            return MutationResponse(
                success=False,
                message=str(e)
            )
