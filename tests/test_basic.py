#!/usr/bin/env python3
"""
Simple test to verify the scheduling system functionality.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Student, Teacher, Course, Room
from src.algorithm import SchedulingEngine


def test_basic_scheduling():
    """Test basic scheduling functionality."""
    print("Testing basic scheduling functionality...")
    
    # Create test data
    student = Student("S001", "Test Student", 9, ["MATH101", "ENG101"])
    teacher = Teacher("T001", "Test Teacher", ["Mathematics", "English"])
    course1 = Course("MATH101", "Algebra I", "Mathematics", 25)
    course2 = Course("ENG101", "English I", "English", 28)
    room = Room("R101", "Test Room", 30, ["Whiteboard"])
    
    # Initialize scheduler
    scheduler = SchedulingEngine()
    scheduler.add_student(student)
    scheduler.add_teacher(teacher)
    scheduler.add_course(course1)
    scheduler.add_course(course2)
    scheduler.add_room(room)
    
    # Run scheduling
    report = scheduler.run_scheduling()
    
    # Verify results
    assert report['summary']['total_students'] == 1
    assert report['summary']['total_courses'] == 2
    
    # Check that courses were assigned teachers
    assigned_courses = report['summary']['assigned_courses']
    assert assigned_courses >= 1, f"Expected at least 1 assigned course, got {assigned_courses}"
    
    print("✅ Basic scheduling test passed!")
    return True


def test_data_models():
    """Test data model functionality."""
    print("Testing data models...")
    
    # Test Student
    student = Student("S001", "Test Student", 9, ["MATH101", "ENG101"])
    assert student.get_preference_rank("MATH101") == 0
    assert student.get_preference_rank("ENG101") == 1
    assert student.get_preference_rank("INVALID") == -1
    
    student.add_assigned_class("MATH101")
    assert student.has_assigned_class("MATH101")
    assert not student.has_assigned_class("ENG101")
    
    # Test Teacher
    teacher = Teacher("T001", "Test Teacher", ["Mathematics", "English"])
    assert teacher.can_teach("Mathematics")
    assert teacher.can_teach("English")
    assert not teacher.can_teach("Science")
    assert teacher.is_available(1)
    assert teacher.can_take_class()
    
    # Test Course
    course = Course("MATH101", "Algebra I", "Mathematics", 25)
    assert course.can_enroll_student()
    assert course.enroll_student("S001")
    assert course.has_student("S001")
    assert course.get_enrollment_count() == 1
    
    # Test Room
    room = Room("R101", "Test Room", 30, ["Whiteboard", "Computer"])
    assert room.is_available(1)
    assert room.can_accommodate_course(25, ["Whiteboard"])
    assert not room.can_accommodate_course(35, ["Whiteboard"])  # Over capacity
    assert not room.can_accommodate_course(25, ["Lab Equipment"])  # Missing equipment
    
    assert room.assign_course(1, "MATH101")
    assert not room.is_available(1)
    assert room.schedule[1] == "MATH101"
    
    print("✅ Data models test passed!")
    return True


def main():
    """Run all tests."""
    print("🧪 Running Sheridan Scheduling System Tests")
    print("=" * 45)
    
    try:
        test_data_models()
        test_basic_scheduling()
        
        print("\n🎉 All tests passed!")
        return 0
    
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())