import sys
import json
import math

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

def calculate_duration(json_data):
    series = json_data.get("series", [])
    if series:
        fields = series[0].get("fields", [])
        duration_index = None
        for index, field in enumerate(fields):
            if field["name"] == "duration":
                duration_index = index
                break
        
        if duration_index is not None:
            duration_values = fields[duration_index]["values"]
            duration_sum = sum(duration_values)
            duration_min = duration_sum / 1000 / 60 
            duration_hour = duration_min / 60
            print("Sum of duration values (in min):", duration_min)
            print("Sum of duration values (in hours):", duration_hour)
            floor_duration_hour = math.floor(duration_hour)
            real_duration_min = duration_min - (floor_duration_hour * 60)
            print(f"Time in hours and min is: {duration_hour} : {real_duration_min} ")
        else:
            print("Duration field not found.")
    else:
        print("No series found in JSON data.")


def count_distinct_task_id_values(json_data):
    series = json_data.get("series", [])
    if series:
        fields = series[0].get("fields", [])
        task_id_index = None
        for index, field in enumerate(fields):
            if field["name"] == "task_id":
                task_id_index = index
                break
        
        if task_id_index is not None:
            task_id_values = fields[task_id_index]["values"]
            distinct_task_id_values = set(task_id_values)
            distinct_task_id_count = len(distinct_task_id_values)
            print("Count of distinct task_id values:", distinct_task_id_count)
        else:
            print("task_id field not found.")
    else:
        print("No series found in JSON data.")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    json_data = read_json_file(json_file_path)
    if json_data:
        calculate_duration(json_data)
        count_distinct_task_id_values(json_data)
