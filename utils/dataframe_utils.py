import pandas as pd
import json
from utils.config import COL_DICT
import numpy as np
import os
from datetime import datetime

def load_logs(log_file):
    """Load logs from a JSON file."""
    with open(log_file, 'r') as file:
        return json.load(file)

def get_all_date_folders(base_dir):
    """Get all date folders within a directory, sorted by date (newest first)."""
    date_folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]
    # Assumes ISO 8601 date format (YYYY-MM-DD)
    date_folders.sort(reverse=True)
    return [os.path.join(base_dir, folder) for folder in date_folders]

def load_log_files(log_dir, model_tag, freq="10"):
    """Load and parse log files from all date folders, sorted by date (newest first)."""
    date_folders = get_all_date_folders(log_dir)
    log_files = []

    for folder in date_folders:
        try:
            all_files = os.listdir(folder)
        except FileNotFoundError:
            continue  # Skip if folder was removed or inaccessible

        if model_tag == "llm":
            matching_files = [f for f in all_files if f"eval_logs_llm" in f and f"{freq}_eval_logs" in f and f.endswith('.json')]
        elif model_tag == "original":
            matching_files = [f for f in all_files if f"eval_logs_original" in f and f"{freq}_eval_logs" in f and f.endswith('.json')]
        else:
            raise ValueError("Invalid model_tag. Use 'llm' or 'original'.")

        log_files.extend([os.path.join(folder, f) for f in matching_files])

    if not log_files:
        raise FileNotFoundError(f"No matching log files found for model_tag='{model_tag}' and freq='{freq}'")

    # Load the most recent log file
    print("Filtered and sorted log files:", log_files)
    print("Loading log file (first in list):", log_files[0])
    log_file = load_logs(log_files[0])

    return log_file



def extract_data(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    classic_count = 0
    l4s_count = 0
    print("Total steps",len(logs['steps']))
    for step_log in logs['steps']:
        queue_type = step_log['states'][0][0][COL_DICT['queue_type']]
        # print("step_log['states'][0][0][COL_DICT['queue_type']]",step_log['states'][0][0][COL_DICT['queue_type']])
        if queue_type == 0:
            classic_count += 1
        if queue_type == 1:
            l4s_count += 1
        # print("step_log['states'][0][0][COL_DICT['current_queue_delay']]",step_log['states'][0][0][COL_DICT['current_queue_delay']])
        # print("step_log['labels']",step_log['labels'])
        if step_log['labels'][0][0] == 1 or step_log['labels'][0][0] == 2:            
            print("===============34826482374682376428374678623816238")
        if step_log['labels'][0][0] == 0 or step_log['labels'][0][0] == 2:
            steps.append(step_log['step'])
            queue_delays.append(step_log['states'][0][0][COL_DICT['current_queue_delay']])
            packet_lengths.append(step_log['states'][0][0][COL_DICT['packet_length']])
            losses.append(step_log['test_loss'])
            # print(step_log['returns'][0][0][0])
    print("classic_count",classic_count)
    print("l4s_count",l4s_count)
    print("Total steps",len(logs['steps']))
    return steps, queue_delays, packet_lengths, losses


def extract_data_classic(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    classic_count = 0
    l4s_count = 0
    for step_log in logs['steps']:
        queue_type = step_log['states'][0][0][COL_DICT['queue_type']]
        # print("step_log['states'][0][0][COL_DICT['queue_type']]",step_log['states'][0][0][COL_DICT['queue_type']])
        if queue_type == 0:
            classic_count += 1
        if queue_type == 1:
            l4s_count += 1
        # print("step_log['states'][0][0][COL_DICT['current_queue_delay']]",step_log['states'][0][0][COL_DICT['current_queue_delay']])
        # print("step_log['labels']",step_log['labels'])
        if step_log['labels'][0][0] == 1 or step_log['labels'][0][0] == 2:            
            print("===============34826482374682376428374678623816238")
        if queue_type == 0 and (step_log['labels'][0][0] == 0 or step_log['labels'][0][0] == 2):
            steps.append(step_log['step'])
            queue_delays.append(step_log['states'][0][0][COL_DICT['current_queue_delay']])
            packet_lengths.append(step_log['states'][0][0][COL_DICT['packet_length']])
            losses.append(step_log['test_loss'])
            # print(step_log['returns'][0][0][0])
    print("classic_count",classic_count)
    print("l4s_count",l4s_count)
    print("Total steps",len(logs['steps']))
    return steps, queue_delays, packet_lengths, losses


def extract_data_l4s(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    classic_count = 0
    l4s_count = 0
    for step_log in logs['steps']:
        queue_type = step_log['states'][0][0][COL_DICT['queue_type']]
        # print("step_log['states'][0][0][COL_DICT['queue_type']]",step_log['states'][0][0][COL_DICT['queue_type']])
        if queue_type == 0:
            classic_count += 1
        if queue_type == 1:
            l4s_count += 1
        # print("step_log['states'][0][0][COL_DICT['current_queue_delay']]",step_log['states'][0][0][COL_DICT['current_queue_delay']])
        # print("step_log['labels']",step_log['labels'])
        if step_log['labels'][0][0] == 1 or step_log['labels'][0][0] == 2:            
            print("===============34826482374682376428374678623816238")
        # else:
        #     print("***************34826482374682376428374678623816238")
        if queue_type == 1 and (step_log['labels'][0][0] == 0 or step_log['labels'][0][0] == 2):
            steps.append(step_log['step'])
            queue_delays.append(step_log['states'][0][0][COL_DICT['current_queue_delay']])
            packet_lengths.append(step_log['states'][0][0][COL_DICT['packet_length']])
            losses.append(step_log['test_loss'])
            # print(step_log['returns'][0][0][0])
    print("classic_count",classic_count)
    print("l4s_count",l4s_count)
    print("Total steps",len(logs['steps']))
    return steps, queue_delays, packet_lengths, losses

def return_extract_data(logs):
    """Extract steps, queue delays, packet lengths, and test losses from logs."""
    steps, queue_delays, packet_lengths, losses = [], [], [], []
    returns = []
    for step_log in logs['steps']:
        queue_type = step_log['states'][0][0][COL_DICT['queue_type']]
        print("step_log['states'][0][0][COL_DICT['queue_type']]",step_log['states'][0][0][COL_DICT['queue_type']])
        if step_log['labels'] == 0 and step_log['labels'] == 2:
            print("step_log['states'][0][0][COL_DICT['current_queue_delay']]",step_log['states'][0][0][COL_DICT['current_queue_delay']])
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

    print("|||||----" * 50)
    # print(data['Original Queue Delay'].describe())
    # print(data['LLM Queue Delay'].describe())

    print("Original queue delay(ms) median",data['Original Queue Delay'].median()/1000)
    print("LLM queue delay(ms) median",data['LLM Queue Delay'].median()/1000)

    print("Original queue delay(ms) mean",data['Original Queue Delay'].mean()/1000)
    print("LLM queue delay(ms) mean",data['LLM Queue Delay'].mean()/1000)

    # Converting into bits from bytes
    data['LLM Packet Length'] = data['LLM Packet Length'] * 8
    data['Original Packet Length'] = data['Original Packet Length'] * 8
    # Add a base queue delay of 1 ms (1e6 microseconds)
    base_queue_delay_ns = 1e3
    data['Original Queue Delay'] += base_queue_delay_ns
    data['LLM Queue Delay'] += base_queue_delay_ns

    # Convert queue delay from microseconds to seconds
    data['Original Queue Delay'] = data['Original Queue Delay'] / 1e6
    data['LLM Queue Delay'] = data['LLM Queue Delay'] / 1e6

    # Convert packet length from normal bit/bytes to Mb/b
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

    print("Original Throughput median",data['Original Throughput'].median())
    print("LLM Throughput  median",data['LLM Throughput'].median())

    print("Original Throughput mean",data['Original Throughput'].mean())
    print("LLM Throughput mean",data['LLM Throughput'].mean())

    print("addedd 1ms to queue delay for thrpt calculation purposes")

    print("Original queue delay(ms) median",data['Original Queue Delay'].median()*1000)
    print("LLM queue delay(ms) median",data['LLM Queue Delay'].median()*1000)

    print("Original queue delay(ms) mean",data['Original Queue Delay'].mean()*1000)
    print("LLM queue delay(ms) mean",data['LLM Queue Delay'].mean()*1000)


    print("Original Total Data Sent",data['Original Packet Length'].sum())
    print("LLM Total Data Sent",data['LLM Packet Length'].sum())




    # print(data['Original Throughput'].describe())
    # print(data['LLM Queue Delay'].describe())
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
    # print("-" * 50)
    # print("CDF DataFrame Summary:")
    # print(cdf_df.describe())

    import matplotlib.pyplot as plt

    # print(len(data.index))
    # print(data['LLM Queue Delay'])
    # # plt.plot(data.index, data['LLM Queue Delay'])
    # plt.plot(data.index, data['LLM Throughput'], marker ='*')
    # plt.show()
    
    return data, cdf_df


