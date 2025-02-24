# Configuration variables


GRAPH_SAVE_FOLDER = "output/graphs/"
LOG_FILE_ORIGINAL = "G:/Github/1LLM-Results/results/llama3/2025-02-22/llama3_base_eval_logs_original.json"
LOG_FILE_LLM = "G:/Github/1LLM-Results/results/llama3/2025-02-22/llama3_base_eval_logs_llm.json"
DATA_FOLDER = "G:/Github/1LLM-Results/results"


SAVE_FORMATS = ['png', 'eps', 'pdf']  # Formats to save graphs
DPI = 500

# # Color, marker, and linestyle options
# colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '#ff6347']  # Add more colors as needed

colors = ['red','black', 'g', 'm', 'y', 'k']
markers = ['o', 's', 'D', '^', 'v', 'p', '*', 'x']         # Add more markers as needed
linestyles = ['-', '--', '-.', ':']                         # Add more linestyles as needed


bar_width = 0.3

figsize = (8,6)

title_req = False

COL_DICT = {
    'queue_type': 0,
    'burst_allowance': 1,
    'drop_probability': 2,
    'current_queue_delay': 3,
    'accumulated_probability': 4,
    'length_in_bytes': 5,
    'packet_length': 6
}

