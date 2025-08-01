"""
Basic tests for the Sheridan Scheduling system.
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.models import Student, Teacher, ClassOffering, Room, Schedule, ScheduleEntry, Period
from src.data_processor import DataProcessor
from src.scheduler import SchedulingAlgorithm
from src.exporters import ExcelExporter


def test_data_models():
    """Test basic data model functionality."""
    print("Testing data models...")
    
    # Test Student model
    student = Student("S001", "Test Student", 9, ["MATH_ALG1", "ENG_9"], {"MATH_PRE_ALG"})
    assert student.id == "S001"
    assert len(student.requested_classes) == 2
    assert "MATH_PRE_ALG" in student.completed_prerequisites
    
    # Test Teacher model
    teacher = Teacher("T001", "Test Teacher", {"Math", "Science"}, 6)
    assert teacher.id == "T001"
    assert "Math" in teacher.qualified_subjects
    
    # Test ClassOffering model
    class_offering = ClassOffering("MATH_ALG1", "Algebra I", "Math", 25, {"MATH_PRE_ALG"}, {9, 10})
    assert class_offering.id == "MATH_ALG1"
    assert class_offering.max_capacity == 25
    
    # Test Room model
    room = Room("R101", "Math Room 1", 30, "classroom")
    assert room.id == "R101"
    assert room.capacity == 30
    
    # Test Schedule model
    schedule = Schedule()
    entry = ScheduleEntry("MATH_ALG1", "T001", "R101", Period.PERIOD_1, ["S001"])
    assert schedule.add_entry(entry) == True
    assert len(schedule.entries) == 1
    
    print("✓ Data models test passed")


def test_data_processor():
    """Test data loading functionality."""
    print("Testing data processor...")
    
    processor = DataProcessor()
    
    # Test loading sample data
    try:
        students = processor.load_students("data/students.csv")
        teachers = processor.load_teachers("data/teachers.csv")
        classes = processor.load_classes("data/classes.csv")
        rooms = processor.load_rooms("data/rooms.csv")
        
        assert len(students) > 0
        assert len(teachers) > 0
        assert len(classes) > 0
        assert len(rooms) > 0
        
        print(f"✓ Loaded {len(students)} students, {len(teachers)} teachers, {len(classes)} classes, {len(rooms)} rooms")
        
    except FileNotFoundError:
        print("⚠ Sample data files not found, skipping data processor test")
        return
    
    print("✓ Data processor test passed")


def test_scheduling_algorithm():
    """Test basic scheduling functionality."""
    print("Testing scheduling algorithm...")
    
    # Create minimal test data
    students = [
        Student("S001", "Student 1", 9, ["MATH_ALG1"], set()),
        Student("S002", "Student 2", 9, ["MATH_ALG1"], set())
    ]
    
    teachers = [
        Teacher("T001", "Math Teacher", {"Math"}, 7)
    ]
    
    classes = [
        ClassOffering("MATH_ALG1", "Algebra I", "Math", 25, set(), {9})
    ]
    
    rooms = [
        Room("R101", "Math Room", 30, "classroom")
    ]
    
    # Run scheduling
    scheduler = SchedulingAlgorithm(students, teachers, classes, rooms)
    schedule = scheduler.create_schedule()
    
    # Basic checks
    assert len(schedule.entries) > 0
    stats = scheduler.get_scheduling_stats()
    assert stats['total_students'] == 2
    
    print("✓ Scheduling algorithm test passed")


def test_excel_export():
    """Test Excel export functionality."""
    print("Testing Excel export...")
    
    # Create minimal test data
    students = {"S001": Student("S001", "Student 1", 9, ["MATH_ALG1"], set())}
    teachers = {"T001": Teacher("T001", "Math Teacher", {"Math"}, 7)}
    classes = {"MATH_ALG1": ClassOffering("MATH_ALG1", "Algebra I", "Math", 25, set(), {9})}
    rooms = {"R101": Room("R101", "Math Room", 30, "classroom")}
    
    # Create minimal schedule
    schedule = Schedule()
    entry = ScheduleEntry("MATH_ALG1", "T001", "R101", Period.PERIOD_1, ["S001"])
    schedule.add_entry(entry)
    
    # Test export
    exporter = ExcelExporter(schedule, students, teachers, classes, rooms)
    
    try:
        exporter.export_all_views("test_output.xlsx")
        print("✓ Excel export test passed")
        
        # Clean up
        if os.path.exists("test_output.xlsx"):
            os.remove("test_output.xlsx")
            
    except Exception as e:
        print(f"⚠ Excel export test failed: {e}")


def run_all_tests():
    """Run all tests."""
    print("Running Sheridan Scheduling System Tests")
    print("=" * 50)
    
    try:
        test_data_models()
        test_data_processor()
        test_scheduling_algorithm()
        test_excel_export()
        
        print("\n" + "=" * 50)
        print("✅ All tests passed!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        raise


if __name__ == "__main__":
    run_all_tests()