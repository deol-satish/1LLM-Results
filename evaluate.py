import os
from utils.config import GRAPH_SAVE_FOLDER, LOG_FILE_ORIGINAL, LOG_FILE_LLM
from utils.dataframe_utils import create_dataframe,load_logs, extract_data
from utils.plotter import plot_line_comparison, plot_box_comparison, cdf_plot_line_comparison



model_list = ['llama3', 'llama2' , 'opt', 'gpt2', 't5']
model_tag = "llama3"
eval_tag = f"{model_tag}_eval_100_freq"
# Ensure the save folders exist



for model_tag in model_list:

    # Load and extract data
    original_logs = load_logs(LOG_FILE_ORIGINAL)
    llm_logs = load_logs(LOG_FILE_LLM)
    steps_original, queue_delays_original, packet_lengths_original, losses_original = extract_data(original_logs)
    steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm = extract_data(llm_logs)

    # Create DataFrame
    df, cdf_df = create_dataframe(steps_original, queue_delays_original, packet_lengths_original, losses_original,
                            steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm)

    # Add a tag to the folder for better organization
    tagged_folder = os.path.join(GRAPH_SAVE_FOLDER, eval_tag)

    # Ensure the tagged folder exists
    os.makedirs(tagged_folder, exist_ok=True)




    # Plot queue delay comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Traditional L4S', 'L4S-LLM'],
        xlabel='Step Number',
        ylabel='Queue Delay (s)',
        title=f'Queue Delay Comparison: Traditional vs {model_tag}',
        filename=f"{eval_tag}_queue_delay_comparison",
        folder=tagged_folder
    )

    # Plot queue delay box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Traditional L4S', 'L4S-LLM AQM'],
        ylabel='Queue Delay (s)',
        title=f'Queue Delay Comparison (Box Plot): Traditional vs {model_tag}',
        filename=f"{eval_tag}_queue_delay_box_comparison",
        folder=tagged_folder
    )



    # Plot throughput comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Packet Length', 'LLM Packet Length'],
        labels=['Traditional L4S', 'L4S-LLM AQM'],
        xlabel='Step Number',
        ylabel='Packet Length (Mbit/s)',
        title=f'Packet Length Comparison: Traditional vs {model_tag}',
        filename=f"{eval_tag}_throughput_comparison",
        folder=tagged_folder
    )

    # Plot throughput box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Packet Length', 'LLM Throughput'],
        labels=['Traditional L4S', 'L4S-LLM AQM'],
        ylabel='Packet Length (Mbit/s)',
        title=f'Packet Length Comparison (Box Plot): Traditional vs {model_tag}',
        filename=f"{eval_tag}_throughput_box_comparison",
        folder=tagged_folder
    )

    # Plot throughput comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Traditional L4S', 'L4S-LLM AQM'],
        xlabel='Step Number',
        ylabel='Bandwidth Utilisation (Mbit/s)',
        title=f'Throughput Comparison: Traditional vs {model_tag}',
        filename=f"{eval_tag}_throughput_comparison",
        folder=tagged_folder
    )

    # Plot throughput box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Traditional L4S', 'L4S-LLM AQM'],
        ylabel='Bandwidth Utilisation (Mbit/s)',
        title=f'Bandwidth Utilisation Comparison (Box Plot): Traditional vs {model_tag}',
        filename=f"{eval_tag}_throughput_box_comparison",
        folder=tagged_folder
    )



    # Plot throughput CDF comparison
    cdf_plot_line_comparison(
        cdf_df,
        index_rows='Original Throughput Sorted',
        columns=['Original Throughput CDF', 'LLM Throughput CDF'],
        labels=['Traditional L4S', 'L4S-LLM AQM'],
        xlabel='Bandwidth Utilisation (Mbps)',
        ylabel='CDF',
        title='Bandwidth Utilisation CDF Comparison',
        filename=f"{eval_tag}_throughput_cdf_comparison",
        folder=tagged_folder
    )

    # Plot queue delay CDF comparison
    cdf_plot_line_comparison(
        cdf_df,
        index_rows='Original Queue Delay Sorted',
        columns=['Original Queue Delay CDF', 'LLM Queue Delay CDF'],
        labels=['Traditional L4S', 'L4S-LLM AQM'],
        xlabel='Queue Delay (s)',
        ylabel='CDF',
        title='Queue Delay CDF Comparison',
        filename=f"{eval_tag}_queue_delay_cdf_comparison",
        folder=tagged_folder
    )



