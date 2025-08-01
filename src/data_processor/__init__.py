"""
Data processor for loading student, teacher, class, and room data from CSV/Excel files.
"""

import pandas as pd
from typing import List, Dict, Any, Union
from pathlib import Path
import logging

from ..models import Student, Teacher, ClassOffering, Room

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataProcessor:
    """Handles loading and processing of input data."""
    
    def __init__(self):
        self.students: List[Student] = []
        self.teachers: List[Teacher] = []
        self.classes: List[ClassOffering] = []
        self.rooms: List[Room] = []
    
    def load_students(self, file_path: Union[str, Path]) -> List[Student]:
        """Load student data from CSV/Excel file."""
        try:
            # Try to read as Excel first, then CSV
            try:
                df = pd.read_excel(file_path)
            except:
                df = pd.read_csv(file_path)
            
            students = []
            for _, row in df.iterrows():
                # Parse requested classes (could be comma-separated)
                requested_classes = []
                if pd.notna(row.get('requested_classes', '')):
                    requested_classes = [cls.strip() for cls in str(row['requested_classes']).split(',')]
                
                # Parse completed prerequisites
                prerequisites = set()
                if pd.notna(row.get('completed_prerequisites', '')):
                    prerequisites = {prereq.strip() for prereq in str(row['completed_prerequisites']).split(',')}
                
                student = Student(
                    id=str(row['id']),
                    name=str(row['name']),
                    grade=int(row['grade']),
                    requested_classes=requested_classes,
                    completed_prerequisites=prerequisites
                )
                students.append(student)
            
            self.students = students
            logger.info(f"Loaded {len(students)} students from {file_path}")
            return students
            
        except Exception as e:
            logger.error(f"Error loading students from {file_path}: {e}")
            raise
    
    def load_teachers(self, file_path: Union[str, Path]) -> List[Teacher]:
        """Load teacher data from CSV/Excel file."""
        try:
            # Try to read as Excel first, then CSV
            try:
                df = pd.read_excel(file_path)
            except:
                df = pd.read_csv(file_path)
            
            teachers = []
            for _, row in df.iterrows():
                # Parse qualified subjects (could be comma-separated)
                qualified_subjects = set()
                if pd.notna(row.get('qualified_subjects', '')):
                    qualified_subjects = {subj.strip() for subj in str(row['qualified_subjects']).split(',')}
                
                teacher = Teacher(
                    id=str(row['id']),
                    name=str(row['name']),
                    qualified_subjects=qualified_subjects,
                    max_periods=int(row.get('max_periods', 7))
                )
                teachers.append(teacher)
            
            self.teachers = teachers
            logger.info(f"Loaded {len(teachers)} teachers from {file_path}")
            return teachers
            
        except Exception as e:
            logger.error(f"Error loading teachers from {file_path}: {e}")
            raise
    
    def load_classes(self, file_path: Union[str, Path]) -> List[ClassOffering]:
        """Load class offering data from CSV/Excel file."""
        try:
            # Try to read as Excel first, then CSV
            try:
                df = pd.read_excel(file_path)
            except:
                df = pd.read_csv(file_path)
            
            classes = []
            for _, row in df.iterrows():
                # Parse prerequisites
                prerequisites = set()
                if pd.notna(row.get('prerequisites', '')):
                    prerequisites = {prereq.strip() for prereq in str(row['prerequisites']).split(',')}
                
                # Parse grade levels
                grade_levels = set()
                if pd.notna(row.get('grade_levels', '')):
                    grade_levels = {int(grade) for grade in str(row['grade_levels']).split(',')}
                
                class_offering = ClassOffering(
                    id=str(row['id']),
                    name=str(row['name']),
                    subject=str(row['subject']),
                    max_capacity=int(row['max_capacity']),
                    prerequisites=prerequisites,
                    grade_levels=grade_levels
                )
                classes.append(class_offering)
            
            self.classes = classes
            logger.info(f"Loaded {len(classes)} class offerings from {file_path}")
            return classes
            
        except Exception as e:
            logger.error(f"Error loading classes from {file_path}: {e}")
            raise
    
    def load_rooms(self, file_path: Union[str, Path]) -> List[Room]:
        """Load room data from CSV/Excel file."""
        try:
            # Try to read as Excel first, then CSV
            try:
                df = pd.read_excel(file_path)
            except:
                df = pd.read_csv(file_path)
            
            rooms = []
            for _, row in df.iterrows():
                room = Room(
                    id=str(row['id']),
                    name=str(row['name']),
                    capacity=int(row['capacity']),
                    room_type=str(row.get('room_type', 'general'))
                )
                rooms.append(room)
            
            self.rooms = rooms
            logger.info(f"Loaded {len(rooms)} rooms from {file_path}")
            return rooms
            
        except Exception as e:
            logger.error(f"Error loading rooms from {file_path}: {e}")
            raise
    
    def load_all_data(self, data_dir: Union[str, Path]) -> Dict[str, Any]:
        """Load all data from a directory containing the required files."""
        data_dir = Path(data_dir)
        
        # Look for expected files
        students_file = None
        teachers_file = None
        classes_file = None
        rooms_file = None
        
        for file_path in data_dir.glob("*"):
            name_lower = file_path.name.lower()
            if "student" in name_lower:
                students_file = file_path
            elif "teacher" in name_lower:
                teachers_file = file_path
            elif "class" in name_lower or "course" in name_lower:
                classes_file = file_path
            elif "room" in name_lower:
                rooms_file = file_path
        
        results = {}
        
        if students_file:
            results['students'] = self.load_students(students_file)
        if teachers_file:
            results['teachers'] = self.load_teachers(teachers_file)
        if classes_file:
            results['classes'] = self.load_classes(classes_file)
        if rooms_file:
            results['rooms'] = self.load_rooms(rooms_file)
        
        return results
    
    def validate_data(self) -> List[str]:
        """Validate loaded data for consistency and completeness."""
        issues = []
        
        # Check if we have data for all entities
        if not self.students:
            issues.append("No student data loaded")
        if not self.teachers:
            issues.append("No teacher data loaded")
        if not self.classes:
            issues.append("No class data loaded")
        if not self.rooms:
            issues.append("No room data loaded")
        
        # Validate student requests against available classes
        available_class_ids = {cls.id for cls in self.classes}
        for student in self.students:
            for requested_class in student.requested_classes:
                if requested_class not in available_class_ids:
                    issues.append(f"Student {student.id} requested unavailable class {requested_class}")
        
        # Validate teacher qualifications against class subjects
        available_subjects = {cls.subject for cls in self.classes}
        for teacher in self.teachers:
            unmatched_subjects = teacher.qualified_subjects - available_subjects
            if unmatched_subjects:
                issues.append(f"Teacher {teacher.id} qualified for unavailable subjects: {unmatched_subjects}")
        
        # Check room capacity vs class capacity
        for room in self.rooms:
            for class_offering in self.classes:
                if class_offering.max_capacity > room.capacity:
                    issues.append(f"Class {class_offering.id} capacity ({class_offering.max_capacity}) exceeds room {room.id} capacity ({room.capacity})")
        
        if issues:
            logger.warning(f"Data validation found {len(issues)} issues")
            for issue in issues:
                logger.warning(f"  - {issue}")
        else:
            logger.info("Data validation passed successfully")
        
        return issues