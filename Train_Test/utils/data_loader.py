import os
import json
import numpy as np
import pandas as pd

def load_log_files(log_dir,model_tag):
    """Load and parse log files."""
    if model_tag == "Training":
        log_files = [
            f for f in os.listdir(log_dir)
            if 'train' in f and f.endswith('.json')
        ]
    if model_tag == "Testing":
        log_files = [
            f for f in os.listdir(log_dir)
            if 'test' in f and f.endswith('.json')
        ]
    log_files.sort(key=lambda x: int(x.split('_')[-1].split('.')[0]))
    return log_files

def parse_logs(log_dir, log_files, model_tag):
    """Extract relevant metrics from log files."""
    epoch_numbers = []
    mean_losses, median_losses, mean_accuracies = [], [], []
    mean_cpu_usage, mean_ram_usage = [], []
    mean_gpu_usage, mean_vram_usage = [], []
    mean_disk_read_speed, mean_disk_write_speed = [], []

    mean_timestamps_each_step = []

    start_time = 0
    end_time = 0
    data_json = {}

    for log_file in log_files:
     
        epoch_number = int(log_file.split('_')[-1].split('.')[0])
        epoch_numbers.append(epoch_number)

        with open(os.path.join(log_dir, log_file), 'r') as file:
            data = json.load(file)
            if model_tag == "Training":
                losses = [step['train_loss'] for step in data['steps']]
            if model_tag == "Testing":
                    losses = [step['test_loss'] for step in data['steps']]
            if epoch_number == 0:
                start_time = float(data['steps'][0]['timestamps'])
            
            
            actions_preds = [step['actions_pred'] for step in data['steps']]
            actions = [step['labels'] for step in data['steps']]
            timestamps_each_step = [float(step['timestamps_each_step']) for step in data['steps']]
            mean_timestamps_each_step.append(np.median(timestamps_each_step))

            # Losses
            mean_losses.append(np.mean(losses))
            median_losses.append(np.median(losses))

            # Accuracy
            accuracies = []
            for preds, true_actions in zip(actions_preds, actions):
                preds_array = np.array(preds)
                true_actions_classes = convert_to_classes(np.array(true_actions))
                preds_indices = preds_array.argmax(axis=1).flatten()
                accuracies.append((preds_indices == true_actions_classes).mean())
            mean_accuracies.append(np.mean(accuracies) if accuracies else None)

            # Resource usage
            mean_cpu_usage.append(np.mean([step['CPU Usage'] for step in data['steps']]))
            mean_ram_usage.append(np.mean([step['RAM Usage'] for step in data['steps']]))
            mean_gpu_usage.append(np.mean([step['GPU Usage'] for step in data['steps']]))
            mean_vram_usage.append(np.mean([step['VRAM Usage'] for step in data['steps']]))
            mean_disk_read_speed.append(np.mean([step['Disk Read Speed (MB/s)'] for step in data['steps']]))
            mean_disk_write_speed.append(np.mean([step['Disk Write Speed (MB/s)'] for step in data['steps']]))
            data_json  = data
    end_time = float(data_json['steps'][-1]['timestamps'])

    print("training_time", str((end_time - start_time) / 3600))


    print("start_time",start_time)
    print("end_time",end_time)

    print("log_dir",log_dir)
    
    print("mean_timestamps_each_step",np.median(mean_timestamps_each_step))
    print()
    print("--"*20)
    print()
   
    return pd.DataFrame({
        'Epoch': epoch_numbers,
        'Mean Loss': mean_losses,
        'Median Loss': median_losses,
        'Mean Accuracy': mean_accuracies,
        'Mean CPU Usage': mean_cpu_usage,
        'Mean RAM Usage': mean_ram_usage,
        'Mean GPU Usage': mean_gpu_usage,
        'Mean VRAM Usage': mean_vram_usage,
        'Mean Disk Read Speed': mean_disk_read_speed,
        'Mean Disk Write Speed': mean_disk_write_speed,
    })

# def convert_to_classes(action):
#     """Convert actions to classes."""
#     return np.vectorize(lambda x: 0 if x < 0.5 else 1 if x < 1.5 else 2)(action.flatten())

def convert_to_classes(action):
    """Convert actions to classes."""
    return action
