# %%
import os
from utils.data_loader import load_log_files, parse_logs
from utils.plotter import plot_comparison
from config.settings import GRAPH_SAVE_FOLDER, DATA_FOLDER, SAVE_FORMATS

# llm_tags = ['opt_train', 'gpt_train', 't5llm_train', 'llama_train1', 'llama_train2', 'llama_train3']
# label_name = "Training"
llm_tags = ['llama3', 'llama2' , 'opt', 'gpt2', 't5']

# llm_tags = ['llama3_train', 'opt_train', 'gpt_train', 't5llm_train']
label_name = "Training"
# Create a list to store dataframes for comparison
dfs = []
labels = []

for llm_tag in llm_tags:
    # Paths
    log_dir = os.path.join(DATA_FOLDER, llm_tag)
    print(log_dir, label_name)
    
    # Load and process data
    log_files = load_log_files(log_dir, label_name)
    df = parse_logs( log_files, label_name)
    
    # Append the dataframe and label
    dfs.append(df)
    labels.append(llm_tag.replace("_train",""))


labels = ["Llama3.2","Llama2", "OPT", "GPT2","T5"]

# Ensure the save folder exists
os.makedirs(GRAPH_SAVE_FOLDER, exist_ok=True)

# Save folder for comparison plots
comparison_folder = os.path.join(GRAPH_SAVE_FOLDER, label_name+"comparison")
os.makedirs(comparison_folder, exist_ok=True)

# Plot Mean Loss comparison
plot_comparison(
    dfs, 'Epoch', 'Mean Loss', labels,
    'Mean Loss Comparison over Epochs', 'Epoch', 'Mean Loss',
    "Mean_Loss_Comparison_Train", comparison_folder
)

# Plot Mean Accuracy comparison
plot_comparison(
    dfs, 'Epoch', 'Mean Accuracy', labels,
    'Mean Accuracy Comparison over Epochs', 'Epoch', 'Mean Accuracy',
    "Mean_Accuracy_Comparison_Train", comparison_folder
)
