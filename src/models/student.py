from typing import List, Optional
from dataclasses import dataclass


@dataclass
class Student:
    """Student model with ID, name, grade, and class preferences."""
    
    id: str
    name: str
    grade: int
    class_preferences: List[str]  # List of preferred course IDs in priority order
    assigned_classes: Optional[List[str]] = None  # List of assigned course IDs
    
    def __post_init__(self):
        if self.assigned_classes is None:
            self.assigned_classes = []
    
    def add_assigned_class(self, course_id: str) -> None:
        """Add a course to the student's assigned classes."""
        if course_id not in self.assigned_classes:
            self.assigned_classes.append(course_id)
    
    def get_preference_rank(self, course_id: str) -> int:
        """Get the preference rank for a course (0 = highest priority, -1 = not preferred)."""
        try:
            return self.class_preferences.index(course_id)
        except ValueError:
            return -1
    
    def has_assigned_class(self, course_id: str) -> bool:
        """Check if student is already assigned to a course."""
        return course_id in self.assigned_classes