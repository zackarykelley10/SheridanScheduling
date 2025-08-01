# Sheridan High School Class Scheduling System

A comprehensive student class scheduling system for Sheridan High School's 7-period system. This system automatically assigns students to classes based on their preferences, manages teacher qualifications and availability, handles room assignments, and generates professional Excel reports.

## Features

- **Student-to-Class Assignment**: Automatically assigns students to preferred classes with priority ranking
- **Teacher Assignment**: Matches qualified teachers to courses based on their expertise and availability
- **Room Allocation**: Assigns appropriate rooms based on capacity and equipment requirements
- **Conflict Resolution**: Handles scheduling conflicts, capacity limits, and waitlist management
- **Excel Export**: Generates comprehensive Excel reports with multiple sheets
- **Data Validation**: Validates input data for consistency and completeness

## System Components

### Data Models
- **Student**: ID, name, grade, class preferences, assigned classes
- **Teacher**: ID, name, qualifications, availability, teaching capacity
- **Course**: ID, name, subject, capacity, room requirements, prerequisites
- **Room**: ID, name, capacity, equipment specifications
- **TimeSlot**: 7-period system management with time scheduling

### Core Algorithm
- Preference-based student assignment with conflict resolution
- Load-balanced teacher assignment
- Efficient room allocation
- Capacity management and overflow handling

### Excel Reports
- Individual student schedules
- Master schedule with all assignments
- Teacher schedules and workloads
- Room utilization reports
- Summary statistics

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zackarykelley10/SheridanScheduling.git
cd SheridanScheduling
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python main.py
```

This will use the sample data files in the `data/` directory and generate `sheridan_schedules.xlsx`.

### Custom Data Files
```bash
python main.py --students my_students.csv --teachers my_teachers.csv --courses my_courses.csv --rooms my_rooms.csv --output my_schedules.xlsx
```

### Command Line Options
- `--students FILE`: Path to students CSV file
- `--teachers FILE`: Path to teachers CSV file  
- `--courses FILE`: Path to courses CSV file
- `--rooms FILE`: Path to rooms CSV file
- `--data-dir DIR`: Directory containing data files (default: data)
- `--output FILE`: Output Excel file name (default: sheridan_schedules.xlsx)
- `--verbose`: Enable verbose output showing conflicts and detailed processing

## Data File Formats

### Students CSV (`students.csv`)
```csv
student_id,name,grade,class_preferences
S001,Alice Johnson,9,"MATH101,ENG101,SCI101,PE101,ART101"
```

### Teachers CSV (`teachers.csv`)  
```csv
teacher_id,name,qualifications,max_classes_per_day,available_periods
T001,Ms. Anderson,"Mathematics,Algebra,Geometry",6,"1,2,3,4,5,6"
```

### Courses CSV (`courses.csv`)
```csv
course_id,name,subject,capacity,room_requirements,prerequisites
MATH101,Algebra I,Mathematics,25,"Whiteboard,Calculator",""
```

### Rooms CSV (`rooms.csv`)
```csv
room_id,name,capacity,equipment
R101,Math Classroom A,30,"Whiteboard,Calculator,Projector"
```

## Sample Data

The system includes sample data files in the `data/` directory:
- 10 students across grades 9-12
- 10 teachers with various qualifications
- 19 courses across core subjects
- 11 rooms with different capacities and equipment

## Output

The system generates an Excel file with the following sheets:

1. **Student Schedules**: Individual schedules for each student showing periods, courses, teachers, and rooms
2. **Master Schedule**: Complete course listing with assignments and utilization
3. **Teacher Schedules**: Teacher workloads and room assignments by period
4. **Room Utilization**: Room usage patterns and availability
5. **Summary**: Overall statistics and course utilization metrics

## Algorithm Details

### Scheduling Process
1. **Teacher Assignment**: Qualified teachers are assigned to courses based on subject expertise and availability
2. **Period and Room Assignment**: Courses are assigned time periods and rooms considering conflicts and requirements
3. **Student Enrollment**: Students are enrolled in courses based on preference ranking and availability

### Conflict Resolution
- Time conflicts: Students cannot be in multiple classes during the same period
- Capacity limits: Courses have maximum enrollment limits
- Room requirements: Courses must be assigned to rooms with appropriate equipment
- Teacher availability: Teachers can only teach during their available periods

### Optimization Features
- Load balancing for teacher assignments
- Efficient room allocation based on capacity requirements
- Priority-based student assignment with waitlist management

## Technical Requirements

- Python 3.7+
- pandas >= 1.5.0
- openpyxl >= 3.0.0
- numpy >= 1.20.0

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.