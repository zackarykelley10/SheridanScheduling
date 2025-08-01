"""
Utility functions for the Sheridan Scheduling system.
"""

import logging
from typing import List, Dict, Any
from pathlib import Path


def setup_logging(level: str = "INFO") -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('sheridan_scheduling.log')
        ]
    )


def validate_file_paths(file_paths: Dict[str, str]) -> List[str]:
    """Validate that all required input files exist."""
    errors = []
    required_files = ['students', 'teachers', 'classes', 'rooms']
    
    for file_type in required_files:
        if file_type not in file_paths:
            errors.append(f"Missing {file_type} file path")
        else:
            file_path = Path(file_paths[file_type])
            if not file_path.exists():
                errors.append(f"{file_type.title()} file not found: {file_path}")
            elif not file_path.is_file():
                errors.append(f"{file_type.title()} path is not a file: {file_path}")
    
    return errors


def print_scheduling_report(stats: Dict[str, Any], unassigned_students: Dict[str, List[str]]) -> None:
    """Print a summary report of the scheduling results."""
    print("\n" + "="*60)
    print("SHERIDAN HIGH SCHOOL - SCHEDULING REPORT")
    print("="*60)
    
    print(f"\nOVERALL STATISTICS:")
    print(f"  Total Students: {stats['total_students']}")
    print(f"  Total Class Requests: {stats['total_requests']}")
    print(f"  Successful Assignments: {stats['total_assignments']}")
    print(f"  Unassigned Requests: {stats['total_unassigned']}")
    print(f"  Assignment Success Rate: {stats['assignment_rate']:.1f}%")
    print(f"  Scheduled Class Periods: {stats['scheduled_classes']}")
    
    if unassigned_students:
        print(f"\nUNASSIGNED STUDENT REQUESTS:")
        for student_id, unassigned_classes in unassigned_students.items():
            if unassigned_classes:
                print(f"  Student {student_id}: {', '.join(unassigned_classes)}")
    else:
        print(f"\n✓ All student requests successfully assigned!")
    
    print("\n" + "="*60)


def get_default_file_paths(data_dir: str = "data") -> Dict[str, str]:
    """Get default file paths for input data."""
    data_path = Path(data_dir)
    return {
        'students': str(data_path / "students.csv"),
        'teachers': str(data_path / "teachers.csv"),
        'classes': str(data_path / "classes.csv"),
        'rooms': str(data_path / "rooms.csv")
    }