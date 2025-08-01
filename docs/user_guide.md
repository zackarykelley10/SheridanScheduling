# Sheridan High School Class Scheduling System - User Guide

## Quick Start

### 1. Prepare Your Data

Create four CSV files in a `data` directory:

#### `students.csv`
```csv
id,name,grade,requested_classes,completed_prerequisites
S001,Alice Johnson,9,"MATH_ALG1,ENG_9,SCI_BIO,HIST_WORLD","MATH_PRE_ALG"
S002,Bob Smith,10,"MATH_GEOM,ENG_10,SCI_CHEM,HIST_US","MATH_ALG1,ENG_9"
```

#### `teachers.csv`
```csv
id,name,qualified_subjects,max_periods
T001,Ms. Johnson,"Math,Science",6
T002,Mr. Smith,"English,History",7
```

#### `classes.csv`
```csv
id,name,subject,max_capacity,prerequisites,grade_levels
MATH_ALG1,Algebra I,Math,25,"MATH_PRE_ALG","9,10"
ENG_9,English 9,English,28,"","9"
```

#### `rooms.csv`
```csv
id,name,capacity,room_type
R101,Math Classroom 1,30,classroom
R201,English Classroom 1,32,classroom
```

### 2. Run the Scheduler

```bash
python main.py
```

### 3. Check the Output

The system creates `sheridan_schedule.xlsx` with five sheets:
- **Summary**: Overall statistics
- **Master Schedule**: All classes by period
- **Student Schedules**: Individual student timetables
- **Teacher Schedules**: Teacher assignments
- **Room Schedules**: Room utilization

## Data Preparation Guidelines

### Student Data Tips

1. **Student IDs**: Use unique identifiers (e.g., S001, S002)
2. **Requested Classes**: List class IDs separated by commas
3. **Prerequisites**: List completed classes that unlock advanced courses
4. **Grade Levels**: Use 9, 10, 11, or 12

### Teacher Data Tips

1. **Qualified Subjects**: Match these to the subjects in your class offerings
2. **Max Periods**: Most teachers can teach 6-7 periods per day
3. **Subject Names**: Use consistent naming (e.g., "Math", "Science", "English")

### Class Data Tips

1. **Prerequisites**: Use class IDs that students must have completed
2. **Grade Levels**: Comma-separated list of eligible grades
3. **Capacity**: Consider classroom sizes and pedagogical needs
4. **Subject Matching**: Ensure subjects match teacher qualifications

### Room Data Tips

1. **Capacity**: Should accommodate your largest classes
2. **Room Types**: Use descriptive types (classroom, lab, gym, studio)
3. **Special Rooms**: Ensure labs, gyms, and specialized rooms are appropriately designated

## Understanding the Results

### Assignment Success Rate

The system reports what percentage of student requests were successfully scheduled:
- **90%+ Success**: Excellent - most students got their preferred classes
- **70-89% Success**: Good - minor adjustments may be needed
- **50-69% Success**: Fair - consider adding teachers or rooms
- **<50% Success**: Poor - significant resource constraints exist

### Common Reasons for Unassigned Classes

1. **Insufficient Teachers**: No qualified teachers available for a subject
2. **Room Constraints**: Not enough appropriate rooms
3. **Schedule Conflicts**: Students already have classes in all available periods
4. **Prerequisites Not Met**: Students haven't completed required courses
5. **Grade Level Restrictions**: Students not eligible for requested classes

## Improving Scheduling Results

### Add More Teachers

If many classes are unassigned due to teacher shortages:

```csv
T016,Ms. New Teacher,"Math,Science",7
T017,Mr. Additional,"English,History",6
```

### Increase Room Capacity

If room capacity is limiting enrollment:

```csv
R601,Large Classroom,40,classroom
R602,Flexible Space,35,classroom
```

### Adjust Class Capacities

Reduce class sizes to better fit available rooms:

```csv
MATH_ALG1,Algebra I,Math,20,"MATH_PRE_ALG","9,10"
```

### Balance Teacher Workloads

Ensure teachers aren't overloaded:

```csv
T001,Ms. Johnson,"Math,Science",5
T002,Mr. Smith,"English,History",6
```

## Troubleshooting

### Error: "File not found"

- Ensure CSV files are in the `data` directory
- Check file names: `students.csv`, `teachers.csv`, `classes.csv`, `rooms.csv`
- Verify file permissions

### Error: "Permission denied"

- Make sure you can write to the output directory
- Try running from a different directory
- Check file system permissions

### Warning: "Data validation issues"

Common validation warnings and fixes:

**"Teacher qualified for unavailable subjects"**
- Update teacher qualifications or add missing classes

**"Class capacity exceeds room capacity"**
- Reduce class capacity or use larger rooms

**"Student requested unavailable class"**
- Add the class to your offerings or remove from student requests

### Low Assignment Rates

If < 70% of requests are assigned:

1. **Check teacher coverage**: Ensure all subjects have qualified teachers
2. **Verify room capacity**: Make sure rooms can handle class sizes
3. **Review prerequisites**: Ensure prerequisite chains are reasonable
4. **Balance demand**: Consider if too many students want the same classes

## Advanced Usage

### Custom Data Directory

```bash
python main.py --data-dir custom_data_folder
```

### Custom Output File

```bash
python main.py --output my_schedule.xlsx
```

### Debug Mode

```bash
python main.py --log-level DEBUG
```

### Batch Processing

Create a script to process multiple scenarios:

```bash
#!/bin/bash
python main.py --data-dir scenario1 --output scenario1_schedule.xlsx
python main.py --data-dir scenario2 --output scenario2_schedule.xlsx
python main.py --data-dir scenario3 --output scenario3_schedule.xlsx
```

## Best Practices

### Planning Your Schedule

1. **Start Early**: Begin with basic data and refine iteratively
2. **Test Scenarios**: Try different teacher and room configurations
3. **Validate Prerequisites**: Ensure prerequisite chains make sense
4. **Balance Resources**: Aim for 80-90% teacher and room utilization

### Data Management

1. **Backup Data**: Keep copies of your input files
2. **Version Control**: Track changes to your data files
3. **Document Assumptions**: Note decisions about capacities and assignments
4. **Regular Updates**: Keep teacher qualifications and room data current

### Quality Assurance

1. **Review Reports**: Check the Summary sheet for red flags
2. **Validate Assignments**: Spot-check individual student schedules
3. **Check Conflicts**: Ensure no double-bookings in Master Schedule
4. **Student Feedback**: Consider surveying students about their assigned schedules

## FAQ

**Q: Can I use Excel files instead of CSV?**
A: Yes, the system accepts both CSV and Excel (.xlsx) files.

**Q: What if a teacher is qualified for multiple subjects?**
A: List all subjects separated by commas: "Math,Science,Computer Science"

**Q: How do I handle lunch periods?**
A: The system schedules 7 periods. You can designate one as lunch or handle lunch separately.

**Q: Can students have free periods?**
A: Yes, if a student requests fewer than 7 classes, they'll have free periods.

**Q: What about split/block scheduling?**
A: This system assumes single-period classes. Block scheduling would require modifications.

**Q: How do I handle students with special needs?**
A: You can create specific classes or sections and assign appropriate teachers and rooms.

**Q: Can I limit which periods certain classes are offered?**
A: The current system doesn't support period restrictions, but this could be added as an enhancement.

For technical support or enhancement requests, please refer to the main documentation or contact your system administrator.