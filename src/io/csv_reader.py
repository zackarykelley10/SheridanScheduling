import pandas as pd
from typing import List, Dict, Any
from ..models import Student, Teacher, Course, Room


class CSVDataReader:
    """Reader for CSV/Excel input data files."""
    
    @staticmethod
    def read_students(file_path: str) -> List[Student]:
        """Read student data from CSV file."""
        try:
            df = pd.read_csv(file_path)
            students = []
            
            for _, row in df.iterrows():
                # Parse class preferences from comma-separated string
                preferences = []
                if pd.notna(row.get('class_preferences', '')):
                    preferences = [pref.strip() for pref in str(row['class_preferences']).split(',')]
                
                student = Student(
                    id=str(row['student_id']),
                    name=str(row['name']),
                    grade=int(row['grade']),
                    class_preferences=preferences
                )
                students.append(student)
            
            return students
        except Exception as e:
            raise ValueError(f"Error reading students file {file_path}: {str(e)}")
    
    @staticmethod
    def read_teachers(file_path: str) -> List[Teacher]:
        """Read teacher data from CSV file."""
        try:
            df = pd.read_csv(file_path)
            teachers = []
            
            for _, row in df.iterrows():
                # Parse qualifications from comma-separated string
                qualifications = []
                if pd.notna(row.get('qualifications', '')):
                    qualifications = [qual.strip() for qual in str(row['qualifications']).split(',')]
                
                # Parse available periods
                available_periods = set(range(1, 8))  # Default to all periods
                if pd.notna(row.get('available_periods', '')):
                    periods_str = str(row['available_periods']).strip()
                    if periods_str:
                        available_periods = set(int(p.strip()) for p in periods_str.split(','))
                
                teacher = Teacher(
                    id=str(row['teacher_id']),
                    name=str(row['name']),
                    qualifications=qualifications,
                    max_classes_per_day=int(row.get('max_classes_per_day', 7)),
                    available_periods=available_periods
                )
                teachers.append(teacher)
            
            return teachers
        except Exception as e:
            raise ValueError(f"Error reading teachers file {file_path}: {str(e)}")
    
    @staticmethod
    def read_courses(file_path: str) -> List[Course]:
        """Read course data from CSV file."""
        try:
            df = pd.read_csv(file_path)
            courses = []
            
            for _, row in df.iterrows():
                # Parse room requirements from comma-separated string
                room_requirements = []
                if pd.notna(row.get('room_requirements', '')):
                    room_requirements = [req.strip() for req in str(row['room_requirements']).split(',')]
                
                # Parse prerequisites from comma-separated string
                prerequisites = []
                if pd.notna(row.get('prerequisites', '')):
                    prerequisites = [prereq.strip() for prereq in str(row['prerequisites']).split(',')]
                
                course = Course(
                    id=str(row['course_id']),
                    name=str(row['name']),
                    subject=str(row['subject']),
                    capacity=int(row['capacity']),
                    room_requirements=room_requirements,
                    prerequisites=prerequisites
                )
                courses.append(course)
            
            return courses
        except Exception as e:
            raise ValueError(f"Error reading courses file {file_path}: {str(e)}")
    
    @staticmethod
    def read_rooms(file_path: str) -> List[Room]:
        """Read room data from CSV file."""
        try:
            df = pd.read_csv(file_path)
            rooms = []
            
            for _, row in df.iterrows():
                # Parse equipment from comma-separated string
                equipment = []
                if pd.notna(row.get('equipment', '')):
                    equipment = [eq.strip() for eq in str(row['equipment']).split(',')]
                
                room = Room(
                    id=str(row['room_id']),
                    name=str(row['name']),
                    capacity=int(row['capacity']),
                    equipment=equipment
                )
                rooms.append(room)
            
            return rooms
        except Exception as e:
            raise ValueError(f"Error reading rooms file {file_path}: {str(e)}")
    
    @staticmethod
    def validate_data(students: List[Student], teachers: List[Teacher], 
                     courses: List[Course], rooms: List[Room]) -> List[str]:
        """Validate loaded data for consistency and completeness."""
        errors = []
        
        # Check for duplicate IDs
        student_ids = [s.id for s in students]
        if len(student_ids) != len(set(student_ids)):
            errors.append("Duplicate student IDs found")
        
        teacher_ids = [t.id for t in teachers]
        if len(teacher_ids) != len(set(teacher_ids)):
            errors.append("Duplicate teacher IDs found")
        
        course_ids = [c.id for c in courses]
        if len(course_ids) != len(set(course_ids)):
            errors.append("Duplicate course IDs found")
        
        room_ids = [r.id for r in rooms]
        if len(room_ids) != len(set(room_ids)):
            errors.append("Duplicate room IDs found")
        
        # Check if student preferences reference valid courses
        valid_course_ids = set(course_ids)
        for student in students:
            for pref in student.class_preferences:
                if pref not in valid_course_ids:
                    errors.append(f"Student {student.name} has invalid course preference: {pref}")
        
        # Check if there are enough qualified teachers for courses
        subjects_needed = set(c.subject for c in courses)
        subjects_available = set()
        for teacher in teachers:
            subjects_available.update(teacher.qualifications)
        
        missing_subjects = subjects_needed - subjects_available
        if missing_subjects:
            errors.append(f"No teachers qualified for subjects: {', '.join(missing_subjects)}")
        
        return errors