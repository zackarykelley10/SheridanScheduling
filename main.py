#!/usr/bin/env python3
"""
Sheridan High School Class Scheduling System
Main entry point for the scheduling application.
"""

import argparse
import sys
import os
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.io import CSVDataReader
from src.algorithm import SchedulingEngine
from src.export import ExcelExporter


def main():
    """Main application entry point."""
    parser = argparse.ArgumentParser(
        description="Sheridan High School Class Scheduling System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --students data/students.csv --teachers data/teachers.csv --courses data/courses.csv --rooms data/rooms.csv
  python main.py --data-dir data --output schedules.xlsx
        """
    )
    
    parser.add_argument(
        '--students',
        type=str,
        help='Path to students CSV file'
    )
    
    parser.add_argument(
        '--teachers',
        type=str,
        help='Path to teachers CSV file'
    )
    
    parser.add_argument(
        '--courses',
        type=str,
        help='Path to courses CSV file'
    )
    
    parser.add_argument(
        '--rooms',
        type=str,
        help='Path to rooms CSV file'
    )
    
    parser.add_argument(
        '--data-dir',
        type=str,
        default='data',
        help='Directory containing data files (default: data)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='sheridan_schedules.xlsx',
        help='Output Excel file name (default: sheridan_schedules.xlsx)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    # Determine file paths
    if args.students and args.teachers and args.courses and args.rooms:
        # Use explicitly provided file paths
        students_file = args.students
        teachers_file = args.teachers
        courses_file = args.courses
        rooms_file = args.rooms
    else:
        # Use data directory
        data_dir = Path(args.data_dir)
        students_file = data_dir / 'students.csv'
        teachers_file = data_dir / 'teachers.csv'
        courses_file = data_dir / 'courses.csv'
        rooms_file = data_dir / 'rooms.csv'
    
    try:
        print("🏫 Sheridan High School Class Scheduling System")
        print("=" * 50)
        
        # Load data
        print("📁 Loading data files...")
        if args.verbose:
            print(f"  Students: {students_file}")
            print(f"  Teachers: {teachers_file}")
            print(f"  Courses: {courses_file}")
            print(f"  Rooms: {rooms_file}")
        
        students = CSVDataReader.read_students(str(students_file))
        teachers = CSVDataReader.read_teachers(str(teachers_file))
        courses = CSVDataReader.read_courses(str(courses_file))
        rooms = CSVDataReader.read_rooms(str(rooms_file))
        
        print(f"✅ Loaded {len(students)} students, {len(teachers)} teachers, "
              f"{len(courses)} courses, {len(rooms)} rooms")
        
        # Validate data
        print("🔍 Validating data...")
        validation_errors = CSVDataReader.validate_data(students, teachers, courses, rooms)
        
        if validation_errors:
            print("❌ Data validation errors found:")
            for error in validation_errors:
                print(f"  • {error}")
            return 1
        
        print("✅ Data validation passed")
        
        # Initialize scheduling engine
        print("⚙️  Initializing scheduling engine...")
        scheduler = SchedulingEngine()
        
        # Add data to scheduler
        for student in students:
            scheduler.add_student(student)
        for teacher in teachers:
            scheduler.add_teacher(teacher)
        for course in courses:
            scheduler.add_course(course)
        for room in rooms:
            scheduler.add_room(room)
        
        # Run scheduling algorithm
        print("🔄 Running scheduling algorithm...")
        report = scheduler.run_scheduling()
        
        # Display results
        print("📊 Scheduling Results:")
        print(f"  • Total students: {report['summary']['total_students']}")
        print(f"  • Assigned courses: {report['summary']['assigned_courses']}/{report['summary']['total_courses']}")
        print(f"  • Overall satisfaction rate: {report['summary']['overall_satisfaction_rate']:.1%}")
        print(f"  • Conflicts: {report['summary']['total_conflicts']}")
        print(f"  • Waitlisted students: {report['summary']['waitlisted_students']}")
        
        if args.verbose and report['conflicts']:
            print("\n⚠️  Conflicts:")
            for conflict in report['conflicts']:
                print(f"  • {conflict}")
        
        # Export to Excel
        print(f"📄 Exporting schedules to {args.output}...")
        exporter = ExcelExporter(scheduler.students, scheduler.teachers, 
                                scheduler.courses, scheduler.rooms)
        exporter.export_all_schedules(args.output)
        
        print(f"✅ Schedules exported successfully to {args.output}")
        print("\n🎉 Scheduling complete!")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"❌ File not found: {e}")
        return 1
    except ValueError as e:
        print(f"❌ Data error: {e}")
        return 1
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())