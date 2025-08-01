"""
Core scheduling algorithm for assigning students to classes across 7 periods.
"""

import logging
from typing import List, Dict, Set, Tuple, Optional
from collections import defaultdict
import random

from ..models import Student, Teacher, ClassOffering, Room, Schedule, ScheduleEntry, Period

logger = logging.getLogger(__name__)


class SchedulingAlgorithm:
    """Main scheduling algorithm with conflict resolution."""
    
    def __init__(self, students: List[Student], teachers: List[Teacher], 
                 classes: List[ClassOffering], rooms: List[Room]):
        self.students = {s.id: s for s in students}
        self.teachers = {t.id: t for t in teachers}
        self.classes = {c.id: c for c in classes}
        self.rooms = {r.id: r for r in rooms}
        
        # Track assignments
        self.schedule = Schedule()
        self.student_assignments: Dict[str, Set[str]] = defaultdict(set)  # student_id -> class_ids
        self.unassigned_students: Dict[str, List[str]] = defaultdict(list)  # student_id -> unassigned_class_ids
    
    def create_schedule(self) -> Schedule:
        """Create the complete schedule using a multi-phase approach."""
        logger.info("Starting scheduling process...")
        
        # Phase 1: Create class sections based on demand
        class_sections = self._create_class_sections()
        
        # Phase 2: Assign teachers to class sections
        self._assign_teachers_to_sections(class_sections)
        
        # Phase 3: Assign rooms to class sections
        self._assign_rooms_to_sections(class_sections)
        
        # Phase 4: Schedule sections into periods
        self._schedule_sections_to_periods(class_sections)
        
        # Phase 5: Assign students to specific sections
        self._assign_students_to_sections(class_sections)
        
        logger.info(f"Scheduling complete. Created {len(self.schedule.entries)} scheduled classes.")
        return self.schedule
    
    def _create_class_sections(self) -> Dict[str, List[Dict]]:
        """Create multiple sections for classes based on student demand."""
        logger.info("Creating class sections based on student demand...")
        
        # Count student demand for each class
        class_demand = defaultdict(list)
        for student in self.students.values():
            for class_id in student.requested_classes:
                if class_id in self.classes:
                    # Check prerequisites
                    class_offering = self.classes[class_id]
                    if self._check_prerequisites(student, class_offering):
                        if not class_offering.grade_levels or student.grade in class_offering.grade_levels:
                            class_demand[class_id].append(student.id)
        
        # Create sections for each class
        class_sections = defaultdict(list)
        for class_id, interested_students in class_demand.items():
            class_offering = self.classes[class_id]
            num_sections = (len(interested_students) + class_offering.max_capacity - 1) // class_offering.max_capacity
            
            for section_num in range(num_sections):
                section = {
                    'id': f"{class_id}_S{section_num + 1}",
                    'class_id': class_id,
                    'section_number': section_num + 1,
                    'teacher_id': None,
                    'room_id': None,
                    'period': None,
                    'students': [],
                    'max_capacity': class_offering.max_capacity
                }
                class_sections[class_id].append(section)
        
        logger.info(f"Created sections for {len(class_sections)} classes")
        return class_sections
    
    def _assign_teachers_to_sections(self, class_sections: Dict[str, List[Dict]]) -> None:
        """Assign qualified teachers to class sections."""
        logger.info("Assigning teachers to class sections...")
        
        # Find qualified teachers for each subject
        subject_teachers = defaultdict(list)
        for teacher in self.teachers.values():
            for subject in teacher.qualified_subjects:
                subject_teachers[subject].append(teacher.id)
        
        teacher_assignments = defaultdict(int)  # Track teacher workload
        
        for class_id, sections in class_sections.items():
            class_offering = self.classes[class_id]
            qualified_teachers = subject_teachers.get(class_offering.subject, [])
            
            if not qualified_teachers:
                logger.warning(f"No qualified teachers found for {class_offering.subject}")
                continue
            
            for section in sections:
                # Find teacher with lowest current workload
                best_teacher = min(qualified_teachers, 
                                 key=lambda t: teacher_assignments[t])
                
                if teacher_assignments[best_teacher] < self.teachers[best_teacher].max_periods:
                    section['teacher_id'] = best_teacher
                    teacher_assignments[best_teacher] += 1
                else:
                    logger.warning(f"No available teacher for section {section['id']}")
    
    def _assign_rooms_to_sections(self, class_sections: Dict[str, List[Dict]]) -> None:
        """Assign rooms to class sections."""
        logger.info("Assigning rooms to class sections...")
        
        # Sort rooms by capacity (prefer smaller rooms when possible)
        sorted_rooms = sorted(self.rooms.values(), key=lambda r: r.capacity)
        
        for class_id, sections in class_sections.items():
            class_offering = self.classes[class_id]
            
            for section in sections:
                # Find smallest room that can accommodate the class
                for room in sorted_rooms:
                    if room.capacity >= class_offering.max_capacity:
                        section['room_id'] = room.id
                        break
                
                if not section['room_id']:
                    logger.warning(f"No suitable room found for section {section['id']}")
    
    def _schedule_sections_to_periods(self, class_sections: Dict[str, List[Dict]]) -> None:
        """Schedule sections into time periods, avoiding conflicts."""
        logger.info("Scheduling sections into time periods...")
        
        # Track period assignments
        period_teachers = {period: set() for period in Period}
        period_rooms = {period: set() for period in Period}
        
        # Flatten all sections and sort by priority (fewer available slots first)
        all_sections = []
        for sections in class_sections.values():
            all_sections.extend(sections)
        
        # Shuffle to avoid bias toward first classes
        random.shuffle(all_sections)
        
        for section in all_sections:
            if not section['teacher_id'] or not section['room_id']:
                continue
            
            # Find available period
            assigned = False
            for period in Period:
                teacher_id = section['teacher_id']
                room_id = section['room_id']
                
                if (teacher_id not in period_teachers[period] and 
                    room_id not in period_rooms[period]):
                    
                    section['period'] = period
                    period_teachers[period].add(teacher_id)
                    period_rooms[period].add(room_id)
                    assigned = True
                    break
            
            if not assigned:
                logger.warning(f"Could not schedule section {section['id']} - no available periods")
    
    def _assign_students_to_sections(self, class_sections: Dict[str, List[Dict]]) -> None:
        """Assign students to specific class sections."""
        logger.info("Assigning students to class sections...")
        
        # Track student schedules to avoid conflicts
        student_periods = {student_id: set() for student_id in self.students.keys()}
        
        # Process each student's requests
        for student in self.students.values():
            for class_id in student.requested_classes:
                if class_id not in class_sections:
                    self.unassigned_students[student.id].append(class_id)
                    continue
                
                # Check prerequisites and grade level
                class_offering = self.classes[class_id]
                if not self._check_prerequisites(student, class_offering):
                    self.unassigned_students[student.id].append(class_id)
                    continue
                
                if class_offering.grade_levels and student.grade not in class_offering.grade_levels:
                    self.unassigned_students[student.id].append(class_id)
                    continue
                
                # Find available section
                assigned = False
                for section in class_sections[class_id]:
                    if (section['period'] and 
                        section['period'] not in student_periods[student.id] and
                        len(section['students']) < section['max_capacity']):
                        
                        section['students'].append(student.id)
                        student_periods[student.id].add(section['period'])
                        self.student_assignments[student.id].add(class_id)
                        assigned = True
                        break
                
                if not assigned:
                    self.unassigned_students[student.id].append(class_id)
        
        # Create schedule entries from sections
        for sections in class_sections.values():
            for section in sections:
                if (section['teacher_id'] and section['room_id'] and 
                    section['period'] and section['students']):
                    
                    entry = ScheduleEntry(
                        class_id=section['class_id'],
                        teacher_id=section['teacher_id'],
                        room_id=section['room_id'],
                        period=section['period'],
                        students=section['students'].copy()
                    )
                    self.schedule.add_entry(entry)
    
    def _check_prerequisites(self, student: Student, class_offering: ClassOffering) -> bool:
        """Check if student has completed prerequisites for a class."""
        return class_offering.prerequisites.issubset(student.completed_prerequisites)
    
    def get_scheduling_stats(self) -> Dict[str, int]:
        """Get statistics about the scheduling results."""
        total_students = len(self.students)
        total_requests = sum(len(s.requested_classes) for s in self.students.values())
        total_assignments = sum(len(assignments) for assignments in self.student_assignments.values())
        total_unassigned = sum(len(unassigned) for unassigned in self.unassigned_students.values())
        
        return {
            'total_students': total_students,
            'total_requests': total_requests,
            'total_assignments': total_assignments,
            'total_unassigned': total_unassigned,
            'assignment_rate': (total_assignments / total_requests) * 100 if total_requests > 0 else 0,
            'scheduled_classes': len(self.schedule.entries)
        }