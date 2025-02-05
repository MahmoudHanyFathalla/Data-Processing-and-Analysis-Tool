import sys
import json
import math
import csv
import statistics
from datetime import datetime
import mysql.connector

# Global variables to store calculated values
global_mean_duration = 0
global_stdev_duration = 0
global_max_duration = 0
global_min_duration = 0
global_floor_duration_hour = 0
global_real_duration_min = 0
global_distinct_task_id_count = 0
global_repetition_counts_sum = 0
global_project_names = {}
global_start_time = ""
global_end_time = ""
global_unique_usernames = set()
global_start_hour = 0
global_start_minute = 0
global_end_hour = 0
global_end_minute = 0
global_start_date = ""
global_end_date = ""


def read_json_file(file_path):
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
            print("File found.")
            return data
    except FileNotFoundError:
        print("File not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format.")
        return None


def get_values(results, field_name):
    field_values = []
    for key, value in results.items():
        frames = value.get("frames", [])
        for frame in frames:
            fields = frame.get("schema", {}).get("fields", [])
            index = next((i for i, field in enumerate(fields) if field["name"] == field_name), None)
            if index is not None:
                data_values = frame.get("data", {}).get("values", [])
                field_values.extend(data_values[index])
            else:
                print(f"{field_name} field not found.")
    return field_values


def calculate_duration(json_data):
    global global_mean_duration, global_stdev_duration, global_max_duration, global_min_duration, global_floor_duration_hour, global_real_duration_min

    duration_values = get_values(json_data.get("results", {}), "duration")

    global_mean_duration = statistics.mean(duration_values)
    global_stdev_duration = statistics.stdev(duration_values)
    global_max_duration = max(duration_values)
    global_min_duration = min(duration_values)

    duration_sum = sum(duration_values)
    duration_min = duration_sum / 1000 / 60
    duration_hour = duration_min / 60

    global_floor_duration_hour = math.floor(duration_hour)
    global_real_duration_min = duration_min - (global_floor_duration_hour * 60)


def count_distinct_task_id_values(json_data):
    global global_distinct_task_id_count
    task_id_values = get_values(json_data.get("results", {}), "task_id")
    distinct_task_ids = set(task_id_values)
    global_distinct_task_id_count = len(distinct_task_ids)


def calculate_sum_of_large_frames_inProjecrID(json_data, threshold):
    global global_repetition_counts_sum
    payload_values = get_values(json_data.get("results", {}), "payload")
    task_id_values = get_values(json_data.get("results", {}), "task_id")
    frame_count = {}
    
    for index, payload in enumerate(payload_values):
        try:
            payload_dict = json.loads(payload)
            frame_num = payload_dict.get("frame")
            if frame_num is not None:
                task_id = task_id_values[index]
                calculated_value = task_id * 1000000 + frame_num
                frame_count[calculated_value] = frame_count.get(calculated_value, 0) + 1
        except json.JSONDecodeError:
            print("Error decoding payload:", payload)
    
    global_repetition_counts_sum = sum(1 for count in frame_count.values() if count >= threshold)



def get_project_names_from_csv(json_data, csv_path):
    global global_project_names

    project_id_values = get_values(json_data.get("results", {}), "project_id")

    with open(csv_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        id_name_dict = {row[0]: row[1] for row in csv_reader}

    for project_id in set(project_id_values):
        project_name = id_name_dict.get(str(project_id), "No name found")
        global_project_names[project_id] = project_name


def print_start_and_end_dates(json_data):
    global global_start_hour, global_start_minute, global_end_hour, global_end_minute, global_start_time, global_end_time, global_start_date, global_end_date

    timestamp_values = get_values(json_data.get("results", {}), "timestamp")

    start_timestamp = min(timestamp_values)
    end_timestamp = max(timestamp_values)

    start_date = datetime.fromtimestamp(start_timestamp / 1000)
    end_date = datetime.fromtimestamp(end_timestamp / 1000)

    global_start_time = start_date
    global_end_time = end_date

    # Extracting date from datetime object
    global_start_date = start_date.date()  # Storing the start date
    global_end_date = end_date.date()      # Storing the end date

    global_start_hour = start_date.hour
    global_start_minute = start_date.minute
    global_end_hour = end_date.hour
    global_end_minute = end_date.minute


def print_unique_usernames(json_data):
    global global_unique_usernames
    username_values = get_values(json_data.get("results", {}), "user_name")
    global_unique_usernames.update(username_values)


def insert_values_into_database():
    # Establish connection to the database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="tmsa7",
        database="db"
    )

    # Create a cursor object
    cursor = conn.cursor()

    # Concatenate project IDs and names
    project_ids = list(global_project_names.keys())
    project_names = list(global_project_names.values())
    unique_project_names = []
    for project_id, project_name in global_project_names.items():
        if project_names.count(project_name) > 1 or project_ids.count(project_id) > 1:
            unique_project_name = f"{project_id}-{project_name}"
        else:
            unique_project_name = project_name
        unique_project_names.append(unique_project_name)

    # Insert values into the database table
    # Insert values into the database table
    sql = """
    INSERT INTO data_summary 
    (mean_duration_sec, std_dev_duration_sec, max_duration_sec, min_duration_sec, duration_hours, duration_minutes, distinct_task_id_count, repetition_counts_sum, start_time, end_time, project_id, project_name, username,start_hour, start_minute, end_hour, end_minute,start_date,end_date) 
    VALUES 
    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
    ON DUPLICATE KEY UPDATE 
    mean_duration_sec = VALUES(mean_duration_sec), 
    std_dev_duration_sec = VALUES(std_dev_duration_sec), 
    max_duration_sec = VALUES(max_duration_sec), 
    min_duration_sec = VALUES(min_duration_sec), 
    duration_hours = VALUES(duration_hours), 
    duration_minutes = VALUES(duration_minutes), 
    distinct_task_id_count = VALUES(distinct_task_id_count), 
    repetition_counts_sum = VALUES(repetition_counts_sum), 
    start_time = VALUES(start_time), 
    end_time = VALUES(end_time), 
    project_id = VALUES(project_id), 
    project_name = VALUES(project_name), 
    username = VALUES(username),
    start_hour = VALUES(start_hour), 
    start_minute = VALUES(start_minute), 
    end_hour = VALUES(end_hour), 
    end_minute = VALUES(end_minute),
    start_date = VALUES(start_date),
    end_date = VALUES(end_date)
    """
    cursor.execute(sql, (
        global_mean_duration / 1000, global_stdev_duration / 1000, global_max_duration / 1000, global_min_duration / 1000,
        global_floor_duration_hour, global_real_duration_min, global_distinct_task_id_count,
        global_repetition_counts_sum,
        global_start_time, global_end_time, ', '.join(map(str, project_ids)), ', '.join(map(str, unique_project_names)),
        ', '.join(map(str, global_unique_usernames)), str(global_start_hour), str(global_start_minute),
        str(global_end_hour), str(global_end_minute), str(global_start_date), str(global_end_date)
    ))


    

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <path_to_json_file> <path_to_csv_file> <threshold>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    csv_file_path = sys.argv[2]
    threshold = int(sys.argv[3])

    json_data = read_json_file(json_file_path)
    if json_data:
        calculate_duration(json_data)
        count_distinct_task_id_values(json_data)
        calculate_sum_of_large_frames_inProjecrID(json_data, threshold)
        get_project_names_from_csv(json_data, csv_file_path)
        print_start_and_end_dates(json_data)
        print_unique_usernames(json_data)
        insert_values_into_database()
