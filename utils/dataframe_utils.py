import pandas as pd
import json
from utils.config import COL_DICT
import numpy as np
import os

def load_logs(log_file):
    """Load logs from a JSON file."""
    with open(log_file, 'r') as file:
        return json.load(file)

def get_all_date_folders(base_dir):
    """Get all date folders within a directory, sorted by date (newest first)."""
    date_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    date_folders.sort(reverse=True)  # Assuming ISO 8601 date format (YYYY-MM-DD)
    return [os.path.join(base_dir, folder) for folder in date_folders]

def load_log_files(log_dir, model_tag,freq="100"):
    """Load and parse log files from all date folders, preferring the newest."""
    date_folders = get_all_date_folders(log_dir)
    print("date folders")
    print(date_folders)
    log_files = []

    folder = date_folders[0]
    if model_tag == "llm":
        current_files = [f for f in os.listdir(folder) if 'eval_logs_llm' in f and f.endswith('.json')]
    elif model_tag == "original":
        current_files = [f for f in os.listdir(folder) if 'eval_logs_original' in f and f.endswith('.json')]
    else:
        raise ValueError("Invalid model_tag. Use 'Training' or 'Testing'.")
    


    for f in current_files:
        log_files.append(os.path.join(folder,f))
    
    # Filter log files to include only those with '100' in the filename
    log_files = [f for f in log_files if f"{freq}_eval_logs" in f]
    # print("***"*20)
    # print(log_files[0])
    # print("***"*20)

    return load_logs(log_files[0])


def extract_data(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    for step_log in logs['steps']:
        steps.append(step_log['step'])
        queue_delays.append(step_log['states'][0][0][COL_DICT['current_queue_delay']])
        packet_lengths.append(step_log['states'][0][0][COL_DICT['packet_length']])
        losses.append(step_log['test_loss'])
    return steps, queue_delays, packet_lengths, losses

def return_extract_data(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    returns = []
    for step_log in logs['steps']:
        steps.append(step_log['step'])
        queue_delays.append(step_log['states'][0][0][COL_DICT['current_queue_delay']])
        packet_lengths.append(step_log['states'][0][0][COL_DICT['packet_length']])
        losses.append(step_log['test_loss'])
        returns.append(step_log['returns'][0][0][0])
        # print(step_log['returns'][0][0][0])
    return steps, queue_delays, packet_lengths, losses, returns

import numpy as np
import pandas as pd

def create_dataframe(steps_original, queue_delays_original, packet_lengths_original, losses_original, 
                     steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm):
    """Create a DataFrame with extracted data, calculate throughput in MB/s, and generate CDFs."""

    # Ensure all data is trimmed to the same minimum length
    min_length = min(len(steps_original), len(queue_delays_original), len(packet_lengths_original),
                     len(losses_original), len(steps_llm), len(queue_delays_llm), 
                     len(packet_lengths_llm), len(losses_llm))

    # Create the main DataFrame
    data = pd.DataFrame({
        'Steps': steps_original[:min_length],
        'Original Loss': losses_original[:min_length],
        'Original Queue Delay': queue_delays_original[:min_length],
        'Original Packet Length': packet_lengths_original[:min_length],
        'LLM Loss': losses_llm[:min_length],
        'LLM Queue Delay': queue_delays_llm[:min_length],
        'LLM Packet Length': packet_lengths_llm[:min_length],
    })

    # print("|||||----" * 50)

    # print(data['Original Queue Delay'].describe())
    # print(data['LLM Queue Delay'].describe())

    # print(data['Original Packet Length'].describe())
    # print(data['LLM Packet Length'].describe())

    # print("|||||----" * 50)

    data['LLM Packet Length'] = data['LLM Packet Length'] * 8
    data['Original Packet Length'] = data['Original Packet Length'] * 8
    # Add a base queue delay of 1 ms (1e6 nanoseconds)
    base_queue_delay_ns = 1e4
    data['Original Queue Delay'] += base_queue_delay_ns
    data['LLM Queue Delay'] += base_queue_delay_ns

    # Convert queue delay from nanoseconds to seconds
    data['Original Queue Delay'] = data['Original Queue Delay'] / 1e6
    data['LLM Queue Delay'] = data['LLM Queue Delay'] / 1e6

    # Convert packet length from bytes to MB
    data['Original Packet Length'] = data['Original Packet Length'] / (1024 * 1034)
    data['LLM Packet Length'] = data['LLM Packet Length'] / (1024 * 1034)

    # print(data['Original Queue Delay'].describe())
    # print(data['LLM Queue Delay'].describe())

    # print(data['Original Packet Length'].describe())
    # print(data['LLM Packet Length'].describe())

    # print("|||||----" * 50)

    # Calculate throughput in MB/s
    data['Original Throughput'] = data['Original Packet Length'] / data['Original Queue Delay']
    data['LLM Throughput'] = data['LLM Packet Length'] / data['LLM Queue Delay']

    # print(data['Original Throughput'].describe())
    # print(data['LLM Throughput'].describe())
    # print("|||||----" * 50)
    # print("|||||----" * 50)
    # print("|||||----" * 50)

    # Replace infinities or NaN values resulting from zero queue delay with 0
    data.replace([np.inf, -np.inf], 0, inplace=True)
    data.fillna(0, inplace=True)

    # # Function to calculate CDF
    # def calculate_cdf(values):
    #     sorted_data = np.sort(values)
    #     cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
    #     return sorted_data, cdf

    # Function to calculate CDF
    def calculate_cdf(values):
        sorted_data = np.sort(values)
        cumulative_data = np.cumsum(sorted_data) / np.sum(sorted_data)
        return sorted_data, cumulative_data

    # Generate CDFs for relevant columns
    cdf_data = {}
    for column in ['Original Loss', 'Original Queue Delay', 'Original Packet Length',
                   'LLM Loss', 'LLM Queue Delay', 'LLM Packet Length', 
                   'Original Throughput', 'LLM Throughput']:
        sorted_data, cdf = calculate_cdf(data[column])
        cdf_data[column + ' Sorted'] = sorted_data
        cdf_data[column + ' CDF'] = cdf

    # Create the CDF DataFrame
    cdf_df = pd.DataFrame(cdf_data)

    # Print summary statistics
    print("-" * 50)
    print("CDF DataFrame Summary:")
    print(cdf_df.describe())
    
    return data, cdf_df


