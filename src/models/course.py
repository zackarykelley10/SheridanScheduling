from typing import List, Optional
from dataclasses import dataclass, field


@dataclass
class Course:
    """Course model with subject, capacity, room requirements, and assignments."""
    
    id: str
    name: str
    subject: str
    capacity: int
    room_requirements: List[str] = field(default_factory=list)  # Equipment/features needed
    prerequisites: List[str] = field(default_factory=list)  # Required prerequisite course IDs
    enrolled_students: List[str] = field(default_factory=list)  # List of enrolled student IDs
    assigned_teacher: Optional[str] = None  # Assigned teacher ID
    assigned_room: Optional[str] = None  # Assigned room ID
    assigned_period: Optional[int] = None  # Assigned time period (1-7)
    
    def can_enroll_student(self) -> bool:
        """Check if course has capacity for another student."""
        return len(self.enrolled_students) < self.capacity
    
    def enroll_student(self, student_id: str) -> bool:
        """Enroll a student in the course if there's capacity."""
        if self.can_enroll_student() and student_id not in self.enrolled_students:
            self.enrolled_students.append(student_id)
            return True
        return False
    
    def is_assigned(self) -> bool:
        """Check if course has teacher, room, and time period assigned."""
        return all([
            self.assigned_teacher is not None,
            self.assigned_room is not None,
            self.assigned_period is not None
        ])
    
    def get_enrollment_count(self) -> int:
        """Get current enrollment count."""
        return len(self.enrolled_students)
    
    def has_student(self, student_id: str) -> bool:
        """Check if a student is enrolled in this course."""
        return student_id in self.enrolled_students