"""
Advanced time conflict detection for appointment scheduling
Used for sophisticated overlap detection with buffer time support
"""

from datetime import datetime, timedelta
from typing import Tuple, Optional


def parse_time(time_str: str) -> datetime:
    """Parse time string (HH:MM) to datetime object"""
    return datetime.strptime(time_str, '%H:%M')


def add_minutes(time_str: str, minutes: int) -> str:
    """Add minutes to time string and return formatted result"""
    time_obj = parse_time(time_str)
    new_time = time_obj + timedelta(minutes=minutes)
    return new_time.strftime('%H:%M')


def time_to_minutes(time_str: str) -> int:
    """Convert HH:MM to minutes since midnight for easier comparison"""
    time_obj = parse_time(time_str)
    return time_obj.hour * 60 + time_obj.minute


def detect_overlap(
    slot1_start: str,
    slot1_duration: int,
    slot2_start: str,
    slot2_duration: int,
    buffer_minutes: int = 5
) -> Tuple[bool, Optional[str]]:
    """
    Sophisticated overlap detection with buffer time
    
    This function checks if two time slots overlap, considering a buffer period
    between appointments. This is critical for preventing double-booking.
    
    Args:
        slot1_start: First appointment start time (HH:MM format)
        slot1_duration: First appointment duration in minutes
        slot2_start: Second appointment start time (HH:MM format)
        slot2_duration: Second appointment duration in minutes
        buffer_minutes: Minimum gap between appointments (default 5 minutes)
    
    Returns:
        Tuple containing:
        - has_conflict (bool): True if time slots overlap
        - conflict_message (str | None): Descriptive message if conflict exists
    
    Example:
        >>> detect_overlap("09:00", 30, "09:20", 30)
        (True, "Conflict detected: Slot 1 (09:00-09:30) overlaps with Slot 2 (09:20-09:50)")
    """
    # Convert to minutes since midnight for easier math
    start1 = time_to_minutes(slot1_start)
    end1 = start1 + slot1_duration + buffer_minutes  # Add buffer after appointment
    
    start2 = time_to_minutes(slot2_start)
    end2 = start2 + slot2_duration + buffer_minutes  # Add buffer after appointment
    
    # Mathematical overlap detection:
    # Two intervals overlap if: start1 < end2 AND start2 < end1
    has_overlap = start1 < end2 and start2 < end1
    
    if has_overlap:
        # Calculate actual end times for display
        slot1_end_time = add_minutes(slot1_start, slot1_duration)
        slot2_end_time = add_minutes(slot2_start, slot2_duration)
        
        message = (
            f"Conflict detected: "
            f"Slot 1 ({slot1_start}-{slot1_end_time}) overlaps with "
            f"Slot 2 ({slot2_start}-{slot2_end_time})"
        )
        return (True, message)
    
    return (False, None)


def validate_business_hours(time_str: str, min_hour: int = 8, max_hour: int = 20) -> bool:
    """
    Validate that appointment time falls within business hours
    
    Args:
        time_str: Time in HH:MM format
        min_hour: Earliest allowed hour (default 8 AM)
        max_hour: Latest allowed hour (default 8 PM)
    
    Returns:
        True if within business hours, False otherwise
    """
    time_obj = parse_time(time_str)
    return min_hour <= time_obj.hour < max_hour
