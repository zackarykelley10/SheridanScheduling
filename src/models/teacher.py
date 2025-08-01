from typing import List, Set
from dataclasses import dataclass, field


@dataclass
class Teacher:
    """Teacher model with qualifications, availability, and teaching capacity."""
    
    id: str
    name: str
    qualifications: List[str]  # List of subjects/courses the teacher can teach
    max_classes_per_day: int = 7  # Maximum classes teacher can teach per day
    available_periods: Set[int] = field(default_factory=lambda: set(range(1, 8)))  # Periods 1-7
    assigned_classes: List[str] = field(default_factory=list)  # List of assigned course IDs
    
    def can_teach(self, subject: str) -> bool:
        """Check if teacher is qualified to teach a subject."""
        return subject in self.qualifications
    
    def is_available(self, period: int) -> bool:
        """Check if teacher is available during a specific period."""
        return period in self.available_periods
    
    def can_take_class(self) -> bool:
        """Check if teacher can take on another class."""
        return len(self.assigned_classes) < self.max_classes_per_day
    
    def assign_class(self, course_id: str) -> bool:
        """Assign a class to the teacher if possible."""
        if self.can_take_class() and course_id not in self.assigned_classes:
            self.assigned_classes.append(course_id)
            return True
        return False
    
    def get_available_periods_list(self) -> List[int]:
        """Get available periods as a sorted list."""
        return sorted(list(self.available_periods))