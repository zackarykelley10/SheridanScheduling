from typing import List, Dict, Optional
from dataclasses import dataclass, field


@dataclass
class Room:
    """Room model with capacity and equipment specifications."""
    
    id: str
    name: str
    capacity: int
    equipment: List[str] = field(default_factory=list)  # Available equipment/features
    schedule: Dict[int, Optional[str]] = field(default_factory=lambda: {i: None for i in range(1, 8)})  # Period -> Course ID
    
    def is_available(self, period: int) -> bool:
        """Check if room is available during a specific period."""
        return period in self.schedule and self.schedule[period] is None
    
    def can_accommodate_course(self, course_capacity: int, required_equipment: List[str]) -> bool:
        """Check if room can accommodate a course's requirements."""
        # Check capacity
        if self.capacity < course_capacity:
            return False
        
        # Check equipment requirements
        for equipment in required_equipment:
            if equipment not in self.equipment:
                return False
        
        return True
    
    def assign_course(self, period: int, course_id: str) -> bool:
        """Assign a course to the room for a specific period."""
        if self.is_available(period):
            self.schedule[period] = course_id
            return True
        return False
    
    def get_schedule(self) -> Dict[int, Optional[str]]:
        """Get the room's schedule."""
        return self.schedule.copy()
    
    def get_available_periods(self) -> List[int]:
        """Get list of available periods."""
        return [period for period, course in self.schedule.items() if course is None]