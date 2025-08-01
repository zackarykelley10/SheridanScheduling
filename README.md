# Sheridan High School Class Scheduling System

An automated Python-based solution for creating student class schedules for a 7-period school day system.

## Features

- **Automated Scheduling**: Intelligently assigns students to their requested classes
- **Conflict Resolution**: Handles scheduling conflicts including:
  - Teacher availability across periods
  - Room capacity and assignment conflicts
  - Student prerequisite requirements
  - Class capacity limits
- **Multi-View Excel Export**: Generates comprehensive Excel reports with:
  - Summary statistics
  - Master schedule (all classes by period)
  - Individual student schedules
  - Teacher schedules
  - Room utilization schedules
- **Data Validation**: Validates input data for consistency and completeness
- **Flexible Input**: Accepts both CSV and Excel input files

## Requirements

- Python 3.8 or higher
- pandas >= 2.0.0
- openpyxl >= 3.1.0

## Installation

1. Clone or download this repository
2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the scheduling system with default settings:

```bash
python main.py
```

This will:
- Load data from the `data/` directory
- Create a schedule
- Export results to `sheridan_schedule.xlsx`

### Advanced Usage

```bash
python main.py --data-dir custom_data --output my_schedule.xlsx --log-level DEBUG
```

**Arguments:**
- `--data-dir`: Directory containing input CSV files (default: `data`)
- `--output`: Output Excel filename (default: `sheridan_schedule.xlsx`)
- `--log-level`: Logging level - DEBUG, INFO, WARNING, ERROR (default: `INFO`)

## Input Data Format

The system expects four CSV files in the data directory:

### 1. Students File (`students.csv`)

| Column | Description | Example |
|--------|-------------|---------|
| id | Unique student identifier | S001 |
| name | Student full name | Alice Johnson |
| grade | Grade level (9-12) | 9 |
| requested_classes | Comma-separated list of class IDs | MATH_ALG1,ENG_9,SCI_BIO |
| completed_prerequisites | Comma-separated list of completed classes | MATH_PRE_ALG |

### 2. Teachers File (`teachers.csv`)

| Column | Description | Example |
|--------|-------------|---------|
| id | Unique teacher identifier | T001 |
| name | Teacher full name | Ms. Johnson |
| qualified_subjects | Comma-separated list of subjects | Math,Science |
| max_periods | Maximum periods teacher can teach | 6 |

### 3. Classes File (`classes.csv`)

| Column | Description | Example |
|--------|-------------|---------|
| id | Unique class identifier | MATH_ALG1 |
| name | Class name | Algebra I |
| subject | Subject area | Math |
| max_capacity | Maximum students per class | 25 |
| prerequisites | Comma-separated prerequisites | MATH_PRE_ALG |
| grade_levels | Comma-separated eligible grades | 9,10 |

### 4. Rooms File (`rooms.csv`)

| Column | Description | Example |
|--------|-------------|---------|
| id | Unique room identifier | R101 |
| name | Room name | Math Classroom 1 |
| capacity | Maximum occupancy | 30 |
| room_type | Type of room | classroom |

## Output

The system generates an Excel workbook with multiple sheets:

1. **Summary**: Overall statistics and scheduling metrics
2. **Master Schedule**: Complete schedule showing all classes by period
3. **Student Schedules**: Individual timetables for each student
4. **Teacher Schedules**: Teaching assignments for each teacher
5. **Room Schedules**: Room utilization throughout the day

## System Architecture

The system is designed with modular components:

- **`src/models/`**: Data models for students, teachers, classes, rooms, and schedules
- **`src/data_processor/`**: Input data loading and validation
- **`src/scheduler/`**: Core scheduling algorithm with conflict resolution
- **`src/exporters/`**: Excel export functionality
- **`src/utils/`**: Utility functions and logging

## Scheduling Algorithm

The system uses a multi-phase scheduling approach:

1. **Demand Analysis**: Calculate student demand for each class
2. **Section Creation**: Create multiple sections based on demand and capacity
3. **Teacher Assignment**: Assign qualified teachers to sections
4. **Room Assignment**: Allocate appropriate rooms to sections
5. **Period Scheduling**: Schedule sections into time periods avoiding conflicts
6. **Student Assignment**: Assign students to specific sections

## Conflict Resolution

The algorithm handles various types of conflicts:

- **Teacher Conflicts**: Ensures teachers are not double-booked
- **Room Conflicts**: Prevents room double-booking
- **Student Conflicts**: Ensures students have only one class per period
- **Prerequisite Validation**: Checks student has completed required prerequisites
- **Capacity Limits**: Respects class and room capacity constraints
- **Grade Level Restrictions**: Ensures students are eligible for requested classes

## Sample Data

The `data/` directory includes sample data files for testing:
- 20 sample students across grades 9-12
- 15 teachers with various subject qualifications
- 29 different class offerings
- 17 rooms with different capacities

## Troubleshooting

### Common Issues

1. **File Not Found**: Ensure CSV files are in the correct directory
2. **Permission Errors**: Make sure you have write permissions for the output directory
3. **Data Validation Warnings**: Review input data for inconsistencies
4. **Low Assignment Rates**: Check for sufficient teachers and rooms for demand

### Logging

Use `--log-level DEBUG` for detailed troubleshooting information.

## Example Run

```bash
$ python main.py
Sheridan High School Class Scheduling System
==================================================
Loading data from data...
INFO:src.data_processor:Loaded 20 students from data/students.csv
INFO:src.data_processor:Loaded 15 teachers from data/teachers.csv
INFO:src.data_processor:Loaded 29 class offerings from data/classes.csv
INFO:src.data_processor:Loaded 17 rooms from data/rooms.csv
Creating class schedule...
INFO:src.scheduler:Starting scheduling process...
INFO:src.scheduler:Scheduling complete. Created 18 scheduled classes.

============================================================
SHERIDAN HIGH SCHOOL - SCHEDULING REPORT
============================================================

OVERALL STATISTICS:
  Total Students: 20
  Total Class Requests: 120
  Successful Assignments: 55
  Unassigned Requests: 65
  Assignment Success Rate: 45.8%
  Scheduled Class Periods: 18
============================================================

Exporting schedule to sheridan_schedule.xlsx...
✓ Schedule export completed: sheridan_schedule.xlsx
```

## Contributing

To extend or modify the system:

1. Follow the modular architecture
2. Add appropriate logging
3. Update documentation
4. Test with sample data

## License

This project is designed for educational use by Sheridan High School.