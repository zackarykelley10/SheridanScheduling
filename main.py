#!/usr/bin/env python3
"""
Sheridan High School Class Scheduling System

This program automates the assignment of students to classes across a 7-period school day,
handling teacher qualifications, room assignments, and conflict resolution.

Usage:
    python main.py [--data-dir DATA_DIR] [--output OUTPUT_FILE] [--log-level LEVEL]

Example:
    python main.py --data-dir data --output schedules.xlsx --log-level INFO
"""

import argparse
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.data_processor import DataProcessor
from src.scheduler import SchedulingAlgorithm
from src.exporters import ExcelExporter
from src.utils import setup_logging, validate_file_paths, print_scheduling_report, get_default_file_paths


def main():
    """Main entry point for the scheduling system."""
    parser = argparse.ArgumentParser(
        description="Sheridan High School Class Scheduling System",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                              # Use default data/ directory and output.xlsx
  %(prog)s --data-dir sample_data       # Use custom data directory
  %(prog)s --output my_schedule.xlsx    # Custom output filename
  %(prog)s --log-level DEBUG            # Enable debug logging
        """
    )
    
    parser.add_argument(
        "--data-dir", 
        default="data",
        help="Directory containing input CSV files (default: data)"
    )
    
    parser.add_argument(
        "--output", 
        default="sheridan_schedule.xlsx",
        help="Output Excel file name (default: sheridan_schedule.xlsx)"
    )
    
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Logging level (default: INFO)"
    )
    
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    
    try:
        print("Sheridan High School Class Scheduling System")
        print("=" * 50)
        
        # Get file paths
        file_paths = get_default_file_paths(args.data_dir)
        
        # Validate input files exist
        validation_errors = validate_file_paths(file_paths)
        if validation_errors:
            print("ERROR: Input file validation failed:")
            for error in validation_errors:
                print(f"  - {error}")
            sys.exit(1)
        
        print(f"Loading data from {args.data_dir}...")
        
        # Load data
        processor = DataProcessor()
        students = processor.load_students(file_paths['students'])
        teachers = processor.load_teachers(file_paths['teachers'])
        classes = processor.load_classes(file_paths['classes'])
        rooms = processor.load_rooms(file_paths['rooms'])
        
        # Validate data consistency
        validation_issues = processor.validate_data()
        if validation_issues:
            print("WARNING: Data validation issues found:")
            for issue in validation_issues:
                print(f"  - {issue}")
            print("Continuing with scheduling...\n")
        
        # Create schedule
        print("Creating class schedule...")
        scheduler = SchedulingAlgorithm(students, teachers, classes, rooms)
        schedule = scheduler.create_schedule()
        
        # Get statistics
        stats = scheduler.get_scheduling_stats()
        unassigned = scheduler.unassigned_students
        
        # Print report
        print_scheduling_report(stats, unassigned)
        
        # Export to Excel
        print(f"\nExporting schedule to {args.output}...")
        exporter = ExcelExporter(
            schedule=schedule,
            students=scheduler.students,
            teachers=scheduler.teachers,
            classes=scheduler.classes,
            rooms=scheduler.rooms
        )
        exporter.export_all_views(args.output)
        
        print(f"✓ Schedule export completed: {args.output}")
        print("\nSchedule includes the following views:")
        print("  - Summary: Overall statistics and metrics")
        print("  - Master Schedule: All classes by period")
        print("  - Student Schedules: Individual student timetables")
        print("  - Teacher Schedules: Teacher assignments by period")
        print("  - Room Schedules: Room utilization by period")
        
    except Exception as e:
        print(f"ERROR: {e}")
        if args.log_level == "DEBUG":
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()