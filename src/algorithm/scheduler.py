from typing import List, Dict, Tuple, Optional
from collections import defaultdict
import random
from ..models import Student, Teacher, Course, Room


class SchedulingEngine:
    """Core scheduling algorithm for student class assignments."""
    
    def __init__(self):
        self.students: Dict[str, Student] = {}
        self.teachers: Dict[str, Teacher] = {}
        self.courses: Dict[str, Course] = {}
        self.rooms: Dict[str, Room] = {}
        self.conflicts: List[str] = []
        self.waitlist: Dict[str, List[str]] = defaultdict(list)  # course_id -> student_ids
    
    def add_student(self, student: Student) -> None:
        """Add a student to the scheduling system."""
        self.students[student.id] = student
    
    def add_teacher(self, teacher: Teacher) -> None:
        """Add a teacher to the scheduling system."""
        self.teachers[teacher.id] = teacher
    
    def add_course(self, course: Course) -> None:
        """Add a course to the scheduling system."""
        self.courses[course.id] = course
    
    def add_room(self, room: Room) -> None:
        """Add a room to the scheduling system."""
        self.rooms[room.id] = room
    
    def run_scheduling(self) -> Dict[str, any]:
        """Run the complete scheduling algorithm."""
        self.conflicts.clear()
        self.waitlist.clear()
        
        # Step 1: Assign teachers to courses
        self._assign_teachers_to_courses()
        
        # Step 2: Assign time periods and rooms to courses
        self._assign_periods_and_rooms()
        
        # Step 3: Assign students to courses based on preferences
        self._assign_students_to_courses()
        
        # Generate scheduling report
        return self._generate_scheduling_report()
    
    def _assign_teachers_to_courses(self) -> None:
        """Assign qualified teachers to courses."""
        unassigned_courses = [c for c in self.courses.values() if c.assigned_teacher is None]
        
        for course in unassigned_courses:
            # Find qualified teachers
            qualified_teachers = [
                t for t in self.teachers.values()
                if t.can_teach(course.subject) and t.can_take_class()
            ]
            
            if qualified_teachers:
                # Assign teacher with least current assignments (load balancing)
                best_teacher = min(qualified_teachers, key=lambda t: len(t.assigned_classes))
                course.assigned_teacher = best_teacher.id
                best_teacher.assign_class(course.id)
            else:
                self.conflicts.append(f"No qualified teacher available for course {course.name}")
    
    def _assign_periods_and_rooms(self) -> None:
        """Assign time periods and rooms to courses."""
        assigned_courses = [c for c in self.courses.values() if c.assigned_teacher is not None]
        
        for course in assigned_courses:
            teacher = self.teachers[course.assigned_teacher]
            best_assignment = self._find_best_period_room_assignment(course, teacher)
            
            if best_assignment:
                period, room_id = best_assignment
                course.assigned_period = period
                course.assigned_room = room_id
                self.rooms[room_id].assign_course(period, course.id)
            else:
                self.conflicts.append(f"No suitable time/room assignment for course {course.name}")
    
    def _find_best_period_room_assignment(self, course: Course, teacher: Teacher) -> Optional[Tuple[int, str]]:
        """Find the best period and room assignment for a course."""
        teacher_available_periods = teacher.get_available_periods_list()
        
        for period in teacher_available_periods:
            # Find suitable rooms for this period
            suitable_rooms = [
                room for room in self.rooms.values()
                if (room.is_available(period) and 
                    room.can_accommodate_course(course.capacity, course.room_requirements))
            ]
            
            if suitable_rooms:
                # Choose room with smallest capacity that can fit the course (efficient allocation)
                best_room = min(suitable_rooms, key=lambda r: r.capacity)
                return period, best_room.id
        
        return None
    
    def _assign_students_to_courses(self) -> None:
        """Assign students to courses based on preferences."""
        # Create a list of (student, course, preference_rank) tuples
        student_course_preferences = []
        
        for student in self.students.values():
            for i, course_id in enumerate(student.class_preferences):
                if course_id in self.courses:
                    course = self.courses[course_id]
                    if course.is_assigned():  # Only consider courses with full assignments
                        student_course_preferences.append((student, course, i))
        
        # Sort by preference rank (lower number = higher priority)
        student_course_preferences.sort(key=lambda x: x[2])
        
        # Assign students to courses
        for student, course, preference_rank in student_course_preferences:
            if self._can_assign_student_to_course(student, course):
                course.enroll_student(student.id)
                student.add_assigned_class(course.id)
            elif course.can_enroll_student():
                # Check for schedule conflicts
                if self._has_schedule_conflict(student, course):
                    self.conflicts.append(
                        f"Schedule conflict: Student {student.name} cannot take {course.name} "
                        f"(Period {course.assigned_period})"
                    )
                else:
                    # Course is full, add to waitlist
                    self.waitlist[course.id].append(student.id)
    
    def _can_assign_student_to_course(self, student: Student, course: Course) -> bool:
        """Check if a student can be assigned to a course."""
        # Check if course has capacity
        if not course.can_enroll_student():
            return False
        
        # Check for schedule conflicts
        if self._has_schedule_conflict(student, course):
            return False
        
        # Check prerequisites (simplified - assumes prerequisites are met)
        # In a real implementation, this would check student's completed courses
        
        return True
    
    def _has_schedule_conflict(self, student: Student, course: Course) -> bool:
        """Check if assigning a student to a course creates a schedule conflict."""
        if course.assigned_period is None:
            return True
        
        # Check if student already has a class in this period
        for assigned_course_id in student.assigned_classes:
            if assigned_course_id in self.courses:
                assigned_course = self.courses[assigned_course_id]
                if assigned_course.assigned_period == course.assigned_period:
                    return True
        
        return False
    
    def _generate_scheduling_report(self) -> Dict[str, any]:
        """Generate a comprehensive scheduling report."""
        total_students = len(self.students)
        total_courses = len(self.courses)
        assigned_courses = len([c for c in self.courses.values() if c.is_assigned()])
        
        student_assignment_stats = {}
        for student in self.students.values():
            assigned_count = len(student.assigned_classes)
            requested_count = len(student.class_preferences)
            student_assignment_stats[student.id] = {
                'assigned': assigned_count,
                'requested': requested_count,
                'satisfaction_rate': assigned_count / requested_count if requested_count > 0 else 0
            }
        
        overall_satisfaction = sum(
            stats['satisfaction_rate'] for stats in student_assignment_stats.values()
        ) / total_students if total_students > 0 else 0
        
        return {
            'summary': {
                'total_students': total_students,
                'total_courses': total_courses,
                'assigned_courses': assigned_courses,
                'overall_satisfaction_rate': overall_satisfaction,
                'total_conflicts': len(self.conflicts),
                'waitlisted_students': sum(len(students) for students in self.waitlist.values())
            },
            'student_assignments': student_assignment_stats,
            'conflicts': self.conflicts,
            'waitlist': dict(self.waitlist),
            'course_enrollments': {
                course_id: {
                    'enrolled_count': course.get_enrollment_count(),
                    'capacity': course.capacity,
                    'utilization_rate': course.get_enrollment_count() / course.capacity
                }
                for course_id, course in self.courses.items()
            }
        }