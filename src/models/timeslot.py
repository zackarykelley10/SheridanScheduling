from dataclasses import dataclass
from typing import Optional


@dataclass
class TimeSlot:
    """TimeSlot model for 7-period system management."""
    
    period: int  # 1-7 for the seven periods
    start_time: str  # Start time in HH:MM format
    end_time: str  # End time in HH:MM format
    name: Optional[str] = None  # Optional period name (e.g., "1st Period", "Lunch")
    
    def __post_init__(self):
        if not 1 <= self.period <= 7:
            raise ValueError("Period must be between 1 and 7")
        
        if self.name is None:
            self.name = f"Period {self.period}"
    
    def duration_minutes(self) -> int:
        """Calculate duration of the time slot in minutes."""
        start_hour, start_min = map(int, self.start_time.split(':'))
        end_hour, end_min = map(int, self.end_time.split(':'))
        
        start_total = start_hour * 60 + start_min
        end_total = end_hour * 60 + end_min
        
        return end_total - start_total
    
    def overlaps_with(self, other: 'TimeSlot') -> bool:
        """Check if this time slot overlaps with another."""
        return self.period == other.period
    
    def __str__(self) -> str:
        return f"{self.name}: {self.start_time} - {self.end_time}"


# Default 7-period schedule for Sheridan High School
DEFAULT_SCHEDULE = [
    TimeSlot(1, "08:00", "08:50", "1st Period"),
    TimeSlot(2, "08:55", "09:45", "2nd Period"),
    TimeSlot(3, "09:50", "10:40", "3rd Period"),
    TimeSlot(4, "10:45", "11:35", "4th Period"),
    TimeSlot(5, "11:40", "12:30", "5th Period"),
    TimeSlot(6, "12:35", "13:25", "6th Period"),
    TimeSlot(7, "13:30", "14:20", "7th Period"),
]