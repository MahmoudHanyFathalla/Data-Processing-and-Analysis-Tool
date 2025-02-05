# JSON Data Processing and Analysis Tool

## Overview

This project is a Python-based tool designed to process and analyze JSON data, particularly focusing on extracting and summarizing key metrics from a JSON file. The tool calculates various statistics such as duration metrics, distinct task IDs, and frame counts, and it also integrates with a CSV file to map project IDs to project names. Additionally, the tool can insert the analyzed data into a MySQL database for further use.

## Features

- **Duration Calculation**: Calculates the mean, standard deviation, maximum, and minimum duration values from the JSON data. It also converts the total duration into hours and minutes.
- **Distinct Task ID Count**: Counts the number of unique task IDs present in the JSON data.
- **Frame Count Analysis**: Analyzes the payload data to count the number of frames that meet a specified threshold.
- **Project Name Mapping**: Maps project IDs to project names using a CSV file.
- **Timestamp Analysis**: Extracts and prints the start and end timestamps from the JSON data.
- **Unique Usernames**: Identifies and prints unique usernames from the JSON data.
- **Database Integration**: Inserts the analyzed data into a MySQL database for persistent storage.

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.x**
- **MySQL Server**
- **Python Libraries**: 
  - `json`
  - `csv`
  - `statistics`
  - `math`
  - `datetime`
  - `mysql.connector`

You can install the required Python libraries using pip:

```bash
pip install mysql-connector-python
```

## Project Structure

The project consists of the following files:

- **code.py**: The main script that processes the JSON data and performs all calculations and analyses.
- **extract_json_data.py**: A more advanced version of the script that includes additional functionality such as database integration and more detailed analysis.
- **newJSON.json**: A sample JSON file containing the data to be processed.
- **save.txt**: A backup or alternative version of the main script.
- **sql code.txt**: Contains the SQL code for creating the database table and inserting sample data.

## Usage

### Running the Script

To run the script, use the following command:

```bash
python code.py <path_to_json_file> <path_to_csv_file> <threshold>
```

- **`<path_to_json_file>`**: The path to the JSON file containing the data to be processed.
- **`<path_to_csv_file>`**: The path to the CSV file containing the project ID to project name mappings.
- **`<threshold>`**: The threshold value for counting frame repetitions in the payload data.

Example:

```bash
python code.py newJSON.json data.csv 5
```

### Database Setup

1. **Create the Database Table**: Use the SQL code provided in `sql code.txt` to create the `data_summary` table in your MySQL database.

2. **Insert Data**: The script will automatically insert the analyzed data into the `data_summary` table. Ensure that the MySQL server is running and accessible.

### Sample JSON Data

The `newJSON.json` file contains sample data that the script can process. The JSON structure includes fields such as `duration`, `task_id`, `payload`, `project_id`, `timestamp`, and `user_name`.

### Sample CSV Data

The CSV file should contain two columns: `project_id` and `project_name`. The script uses this file to map project IDs to their corresponding names.

## Detailed Functionality

### 1. Duration Calculation

The script calculates the following duration metrics:

- **Mean Duration**: The average duration in seconds.
- **Standard Deviation**: The standard deviation of the duration values in seconds.
- **Maximum Duration**: The maximum duration value in seconds.
- **Minimum Duration**: The minimum duration value in seconds.
- **Total Duration**: The total duration converted into hours and minutes.

### 2. Distinct Task ID Count

The script counts the number of unique task IDs present in the JSON data. This helps in understanding the diversity of tasks being performed.

### 3. Frame Count Analysis

The script analyzes the payload data to count the number of frames that meet a specified threshold. This is useful for identifying frames that are repeated multiple times.

### 4. Project Name Mapping

The script maps project IDs to project names using a CSV file. This helps in providing more meaningful insights by replacing project IDs with their corresponding names.

### 5. Timestamp Analysis

The script extracts the start and end timestamps from the JSON data and prints them in a human-readable format. This helps in understanding the time range of the data.

### 6. Unique Usernames

The script identifies and prints unique usernames from the JSON data. This helps in understanding the different users involved in the data.

### 7. Database Integration

The script inserts the analyzed data into a MySQL database. The database table `data_summary` stores metrics such as mean duration, standard deviation, maximum duration, minimum duration, duration in hours and minutes, distinct task ID count, repetition counts, project IDs, project names, start and end times, and unique usernames.

## SQL Table Structure

The `data_summary` table has the following structure:

```sql
CREATE TABLE data_summary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mean_duration_sec FLOAT,
    std_dev_duration_sec FLOAT,
    max_duration_sec FLOAT,
    min_duration_sec FLOAT,
    duration_hours INT,
    duration_minutes FLOAT,
    distinct_task_id_count INT,
    repetition_counts_sum INT,
    project_id VARCHAR(255),
    project_name VARCHAR(255),
    start_time TIME,
    end_time TIME,
    username VARCHAR(255),
    start_hour FLOAT,
    start_minute FLOAT,
    end_hour FLOAT,
    end_minute FLOAT,
    start_date DATE,
    end_date DATE,
    UNIQUE KEY (start_time, username)
);
```

## Example Output

When you run the script, it will print the following information to the console:

- Mean of duration values in seconds.
- Standard deviation of duration values in seconds.
- Maximum duration value in seconds.
- Minimum duration value in seconds.
- Total duration in hours and minutes.
- Count of distinct task IDs.
- Sum of repetition counts for frame values in payload.
- Project names mapped from the CSV file.
- Start and end timestamps.
- Unique usernames.

Additionally, the analyzed data will be inserted into the `data_summary` table in the MySQL database.

## Conclusion

This project provides a comprehensive tool for processing and analyzing JSON data. It offers a wide range of functionalities, from basic statistical calculations to advanced database integration. The tool is highly customizable and can be adapted to various use cases involving JSON data analysis.
