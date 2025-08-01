"""
Data models for the Sheridan Scheduling system.
"""

from dataclasses import dataclass, field
from typing import List, Set, Optional, Dict
from enum import Enum


class Period(Enum):
    """Represents the 7 periods in a school day."""
    PERIOD_1 = 1
    PERIOD_2 = 2
    PERIOD_3 = 3
    PERIOD_4 = 4
    PERIOD_5 = 5
    PERIOD_6 = 6
    PERIOD_7 = 7


@dataclass
class Student:
    """Represents a student with their class preferences."""
    id: str
    name: str
    grade: int
    requested_classes: List[str] = field(default_factory=list)
    completed_prerequisites: Set[str] = field(default_factory=set)
    
    def __post_init__(self):
        """Ensure requested_classes is a list and completed_prerequisites is a set."""
        if isinstance(self.requested_classes, str):
            self.requested_classes = [self.requested_classes]
        if isinstance(self.completed_prerequisites, (list, tuple)):
            self.completed_prerequisites = set(self.completed_prerequisites)


@dataclass
class Teacher:
    """Represents a teacher with their qualifications."""
    id: str
    name: str
    qualified_subjects: Set[str] = field(default_factory=set)
    max_periods: int = 7
    
    def __post_init__(self):
        """Ensure qualified_subjects is a set."""
        if isinstance(self.qualified_subjects, (list, tuple, str)):
            if isinstance(self.qualified_subjects, str):
                self.qualified_subjects = {self.qualified_subjects}
            else:
                self.qualified_subjects = set(self.qualified_subjects)


@dataclass
class ClassOffering:
    """Represents a class that can be offered."""
    id: str
    name: str
    subject: str
    max_capacity: int
    prerequisites: Set[str] = field(default_factory=set)
    grade_levels: Set[int] = field(default_factory=set)
    
    def __post_init__(self):
        """Ensure prerequisites and grade_levels are sets."""
        if isinstance(self.prerequisites, (list, tuple, str)):
            if isinstance(self.prerequisites, str):
                self.prerequisites = {self.prerequisites}
            else:
                self.prerequisites = set(self.prerequisites)
        if isinstance(self.grade_levels, (list, tuple)):
            self.grade_levels = set(self.grade_levels)


@dataclass
class Room:
    """Represents a classroom."""
    id: str
    name: str
    capacity: int
    room_type: str = "general"  # general, lab, gym, etc.


@dataclass
class ScheduleEntry:
    """Represents a single scheduled class period."""
    class_id: str
    teacher_id: str
    room_id: str
    period: Period
    students: List[str] = field(default_factory=list)
    
    def add_student(self, student_id: str) -> bool:
        """Add a student to this class if not already enrolled."""
        if student_id not in self.students:
            self.students.append(student_id)
            return True
        return False
    
    def remove_student(self, student_id: str) -> bool:
        """Remove a student from this class."""
        if student_id in self.students:
            self.students.remove(student_id)
            return True
        return False


@dataclass
class Schedule:
    """Represents the complete school schedule."""
    entries: List[ScheduleEntry] = field(default_factory=list)
    
    def add_entry(self, entry: ScheduleEntry) -> bool:
        """Add a schedule entry if it doesn't conflict."""
        # Check for conflicts
        for existing in self.entries:
            if (existing.period == entry.period and 
                (existing.teacher_id == entry.teacher_id or 
                 existing.room_id == entry.room_id)):
                return False
        
        self.entries.append(entry)
        return True
    
    def get_student_schedule(self, student_id: str) -> List[ScheduleEntry]:
        """Get all classes for a specific student."""
        return [entry for entry in self.entries if student_id in entry.students]
    
    def get_teacher_schedule(self, teacher_id: str) -> List[ScheduleEntry]:
        """Get all classes for a specific teacher."""
        return [entry for entry in self.entries if entry.teacher_id == teacher_id]
    
    def get_room_schedule(self, room_id: str) -> List[ScheduleEntry]:
        """Get all classes for a specific room."""
        return [entry for entry in self.entries if entry.room_id == room_id]
    
    def get_period_schedule(self, period: Period) -> List[ScheduleEntry]:
        """Get all classes for a specific period."""
        return [entry for entry in self.entries if entry.period == period]