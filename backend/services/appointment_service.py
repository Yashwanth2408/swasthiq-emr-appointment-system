"""
Core Appointment Service - Business Logic Layer
This file simulates PostgreSQL operations and implements appointment management.

PRODUCTION NOTES:
- In production, this would interface with Aurora PostgreSQL via SQLAlchemy
- All operations would be wrapped in database transactions
- AppSync subscriptions would trigger on mutations for real-time updates
"""

from datetime import datetime, timedelta
from typing import List, Optional, Dict
from uuid import uuid4
from models.appointment import (
    AppointmentResponse,
    CreateAppointmentInput,
)


# ==============================================
# MOCK DATABASE (Simulating PostgreSQL Tables)
# ==============================================

# In production: This would be Aurora PostgreSQL table
appointments_db: List[Dict] = [
    {
        "id": "apt-001",
        "patient_name": "Rajesh Kumar",
        "date": "2025-12-27",
        "time": "09:00",
        "duration": 30,
        "doctor_name": "Dr. Sarah Johnson",
        "status": "Confirmed",
        "mode": "In-person",
        "created_at": "2025-12-26T10:30:00Z"
    },
    {
        "id": "apt-002",
        "patient_name": "Priya Sharma",
        "date": "2025-12-27",
        "time": "10:00",
        "duration": 45,
        "doctor_name": "Dr. Rajesh Verma",
        "status": "Scheduled",
        "mode": "Video",
        "created_at": "2025-12-26T11:00:00Z"
    },
    {
        "id": "apt-003",
        "patient_name": "Amit Patel",
        "date": "2025-12-27",
        "time": "11:30",
        "duration": 30,
        "doctor_name": "Dr. Sarah Johnson",
        "status": "Upcoming",
        "mode": "In-person",
        "created_at": "2025-12-26T12:00:00Z"
    },
    {
        "id": "apt-004",
        "patient_name": "Sneha Reddy",
        "date": "2025-12-28",
        "time": "14:00",
        "duration": 60,
        "doctor_name": "Dr. Anjali Desai",
        "status": "Confirmed",
        "mode": "In-person",
        "created_at": "2025-12-26T14:30:00Z"
    },
    {
        "id": "apt-005",
        "patient_name": "Vikram Singh",
        "date": "2025-12-26",
        "time": "15:30",
        "duration": 30,
        "doctor_name": "Dr. Sarah Johnson",
        "status": "Completed",
        "mode": "Phone",
        "created_at": "2025-12-25T09:00:00Z"
    },
    {
        "id": "apt-006",
        "patient_name": "Lakshmi Iyer",
        "date": "2025-12-29",
        "time": "09:30",
        "duration": 45,
        "doctor_name": "Dr. Rajesh Verma",
        "status": "Scheduled",
        "mode": "Video",
        "created_at": "2025-12-26T16:00:00Z"
    },
    {
        "id": "apt-007",
        "patient_name": "Arjun Mehta",
        "date": "2025-12-30",
        "time": "11:00",
        "duration": 30,
        "doctor_name": "Dr. Anjali Desai",
        "status": "Scheduled",
        "mode": "In-person",
        "created_at": "2025-12-26T17:00:00Z"
    },
    {
        "id": "apt-008",
        "patient_name": "Kavya Nair",
        "date": "2025-12-25",
        "time": "10:00",
        "duration": 60,
        "doctor_name": "Dr. Sarah Johnson",
        "status": "Cancelled",
        "mode": "In-person",
        "created_at": "2025-12-24T10:00:00Z"
    },
    {
        "id": "apt-009",
        "patient_name": "Rohit Kapoor",
        "date": "2025-12-31",
        "time": "16:00",
        "duration": 30,
        "doctor_name": "Dr. Rajesh Verma",
        "status": "Upcoming",
        "mode": "Video",
        "created_at": "2025-12-26T18:00:00Z"
    },
    {
        "id": "apt-010",
        "patient_name": "Ananya Chatterjee",
        "date": "2026-01-02",
        "time": "09:00",
        "duration": 45,
        "doctor_name": "Dr. Anjali Desai",
        "status": "Scheduled",
        "mode": "In-person",
        "created_at": "2025-12-26T19:00:00Z"
    },
    {
        "id": "apt-011",
        "patient_name": "Deepak Rao",
        "date": "2025-12-28",
        "time": "10:30",
        "duration": 30,
        "doctor_name": "Dr. Sarah Johnson",
        "status": "Confirmed",
        "mode": "In-person",
        "created_at": "2025-12-26T20:00:00Z"
    },
    {
        "id": "apt-012",
        "patient_name": "Neha Gupta",
        "date": "2025-12-29",
        "time": "15:00",
        "duration": 45,
        "doctor_name": "Dr. Anjali Desai",
        "status": "Upcoming",
        "mode": "Video",
        "created_at": "2025-12-26T21:00:00Z"
    },
]


# ==============================================
# UTILITY FUNCTIONS
# ==============================================

def parse_time(time_str: str) -> datetime:
    """Convert time string to datetime for comparison"""
    return datetime.strptime(time_str, '%H:%M')


def calculate_end_time(start_time: str, duration: int) -> str:
    """Calculate end time given start time and duration"""
    start_dt = parse_time(start_time)
    end_dt = start_dt + timedelta(minutes=duration)
    return end_dt.strftime('%H:%M')


def check_time_overlap(start1: str, end1: str, start2: str, end2: str) -> bool:
    """
    Check if two time ranges overlap
    Returns True if there is overlap, False otherwise
    """
    start1_dt = parse_time(start1)
    end1_dt = parse_time(end1)
    start2_dt = parse_time(start2)
    end2_dt = parse_time(end2)
    
    # Check for overlap: intervals overlap if start1 < end2 AND start2 < end1
    return start1_dt < end2_dt and start2_dt < end1_dt


# ==============================================
# CORE SERVICE FUNCTIONS (API Contract)
# ==============================================

def get_appointments(
    date: Optional[str] = None,
    status: Optional[str] = None,
    doctor_name: Optional[str] = None
) -> List[AppointmentResponse]:
    """
    Query appointments with optional filters
    
    PRODUCTION IMPLEMENTATION:
    - Would use SQLAlchemy query with WHERE clauses
    - Indexed on date, doctor_name for performance
    - Pagination with cursor-based approach for large datasets
    
    Args:
        date: Filter by appointment date (YYYY-MM-DD)
        status: Filter by appointment status
        doctor_name: Filter by doctor's name
    
    Returns:
        List of appointments matching filters
    """
    filtered_appointments = appointments_db.copy()
    
    # Apply filters
    if date:
        filtered_appointments = [
            apt for apt in filtered_appointments 
            if apt["date"] == date
        ]
    
    if status:
        filtered_appointments = [
            apt for apt in filtered_appointments 
            if apt["status"] == status
        ]
    
    if doctor_name:
        filtered_appointments = [
            apt for apt in filtered_appointments 
            if apt["doctor_name"] == doctor_name
        ]
    
    # Convert to response models
    return [
        AppointmentResponse(**apt) 
        for apt in filtered_appointments
    ]


def create_appointment(input_data: CreateAppointmentInput) -> AppointmentResponse:
    """
    Create a new appointment with conflict detection
    
    PRODUCTION IMPLEMENTATION:
    - BEGIN TRANSACTION (Isolation: SERIALIZABLE)
    - Acquire row-level lock on doctor's schedule
    - Check conflicts with FOR UPDATE lock
    - INSERT appointment with returning clause
    - COMMIT TRANSACTION
    - Trigger AppSync subscription for real-time UI update
    - Log to audit trail for ABDM compliance
    
    IDEMPOTENCY:
    - Client should send idempotency-key header (UUID)
    - Check DynamoDB cache for duplicate request_id
    - Return cached response if duplicate detected
    
    Args:
        input_data: Validated appointment data from Pydantic model
    
    Returns:
        Created appointment object
    
    Raises:
        ValueError: If time conflict detected or validation fails
    """
    
    # Generate unique ID (in production: database auto-generated)
    new_id = f"apt-{uuid4().hex[:8]}"
    
    # Calculate end time for conflict detection
    new_end_time = calculate_end_time(input_data.time, input_data.duration)
    
    # CONFLICT DETECTION: Check for time overlaps with same doctor
    for existing_apt in appointments_db:
        # Only check same doctor on same date
        if (existing_apt["doctor_name"] == input_data.doctor_name and 
            existing_apt["date"] == input_data.date and
            existing_apt["status"] not in ["Cancelled", "Completed"]):
            
            existing_end_time = calculate_end_time(
                existing_apt["time"], 
                existing_apt["duration"]
            )
            
            # Check for overlap
            if check_time_overlap(
                input_data.time, new_end_time,
                existing_apt["time"], existing_end_time
            ):
                raise ValueError(
                    f"Time conflict: {input_data.doctor_name} already has an appointment "
                    f"from {existing_apt['time']} to {existing_end_time} on {input_data.date}"
                )
    
    # Create new appointment
    new_appointment = {
        "id": new_id,
        "patient_name": input_data.patient_name,
        "date": input_data.date,
        "time": input_data.time,
        "duration": input_data.duration,
        "doctor_name": input_data.doctor_name,
        "status": input_data.status or "Scheduled",
        "mode": input_data.mode,
        "created_at": datetime.utcnow().isoformat() + "Z"
    }
    
    # Add to mock database (in production: INSERT INTO)
    appointments_db.append(new_appointment)
    
    """
    PRODUCTION: Trigger AppSync subscription
    await pubsub.publish(
        topic="appointmentCreated",
        payload=new_appointment
    )
    """
    
    return AppointmentResponse(**new_appointment)


def update_appointment_status(appointment_id: str, new_status: str) -> AppointmentResponse:
    """
    Update appointment status
    
    PRODUCTION IMPLEMENTATION:
    - BEGIN TRANSACTION
    - UPDATE appointments SET status = $1 WHERE id = $2
    - Log status change to audit_log table (ABDM requirement)
    - COMMIT
    - Trigger AppSync subscription for real-time update
    - Send notification (SMS/WhatsApp) if status is Confirmed/Cancelled
    
    Args:
        appointment_id: Unique appointment identifier
        new_status: New status value
    
    Returns:
        Updated appointment object
    
    Raises:
        ValueError: If appointment not found
    """
    for apt in appointments_db:
        if apt["id"] == appointment_id:
            apt["status"] = new_status
            
            """
            PRODUCTION: AppSync subscription trigger
            await pubsub.publish(
                topic=f"appointmentUpdated_{appointment_id}",
                payload={"id": appointment_id, "status": new_status}
            )
            
            ABDM COMPLIANCE: Audit log
            await db.execute(
                INSERT INTO audit_log (entity_type, entity_id, action, user_id, timestamp)
                VALUES ('appointment', $1, 'status_update', $2, NOW())
            )
            """
            
            return AppointmentResponse(**apt)
    
    raise ValueError(f"Appointment with ID {appointment_id} not found")


def delete_appointment(appointment_id: str) -> bool:
    """
    Delete (soft delete in production) an appointment
    
    PRODUCTION IMPLEMENTATION:
    - UPDATE appointments SET deleted_at = NOW() WHERE id = $1
    - Soft delete preserves data for audit compliance
    - Trigger cancellation notifications
    - Update doctor's schedule availability
    
    Args:
        appointment_id: Unique appointment identifier
    
    Returns:
        True if deleted successfully
    
    Raises:
        ValueError: If appointment not found
    """
    for i, apt in enumerate(appointments_db):
        if apt["id"] == appointment_id:
            appointments_db.pop(i)
            
            """
            PRODUCTION: Soft delete
            await db.execute(
                UPDATE appointments 
                SET deleted_at = NOW(), status = 'Cancelled'
                WHERE id = $1
            )
            """
            
            return True
    
    raise ValueError(f"Appointment with ID {appointment_id} not found")


# ==============================================
# DATA CONSISTENCY EXPLANATION
# ==============================================
"""
ENSURING DATA CONSISTENCY IN PRODUCTION:

1. TRANSACTIONS:
   - All mutations wrapped in ACID transactions
   - Isolation level: SERIALIZABLE for conflict detection
   - Row-level locking (SELECT FOR UPDATE) for concurrent access

2. UNIQUE CONSTRAINTS:
   - Database-level constraints on (doctor_id, date, time)
   - UUID primary keys prevent collision
   - Composite indexes on (date, doctor_id) for query performance

3. IDEMPOTENCY KEYS:
   - Client sends X-Idempotency-Key header (UUID)
   - Store in Redis/DynamoDB with 24-hour TTL
   - Return cached response for duplicate requests
   - Prevents double-booking from retry logic

4. OPTIMISTIC LOCKING:
   - Version column (updated_at timestamp)
   - Check version before update
   - Return 409 Conflict if version mismatch

5. ABDM COMPLIANCE:
   - All PHI (Protected Health Information) encrypted at rest
   - Audit trail for all data access
   - Consent artifacts linked to appointments
   - Health ID verification before scheduling

6. APPSYNC SUBSCRIPTIONS:
   - Real-time updates via WebSocket
   - Subscription topics: appointmentCreated, appointmentUpdated, appointmentCancelled
   - Client-side optimistic UI with rollback on conflict
"""
