import os
from utils.config import GRAPH_SAVE_FOLDER, DATA_FOLDER
from utils.dataframe_utils import create_dataframe,load_logs, extract_data,load_log_files, extract_data_classic, extract_data_l4s
from utils.plotter import plot_line_comparison, plot_box_comparison, cdf_plot_line_comparison


# Ensure the save folders exist
llm_tags = ['llama2' , 'llama3','opt', 'gpt2', 't5']
llm_tags = ['llama2']

label_name = "Training"

# Create a list to store dataframes for comparison
dfs = []
labels = []
llmfreq = 10

for llm_tag in llm_tags:
    # Paths
    log_dir = os.path.join(DATA_FOLDER, llm_tag)
    print(log_dir, label_name)

    eval_tag = f"{llm_tag}_eval_{llmfreq}_freq"

    # Load and extract data
    classic_original_logs = load_log_files(log_dir,"original",llmfreq,"classic")
    classic_llm_logs = load_log_files(log_dir,"llm",llmfreq,"classic")

    l4s_original_logs = load_log_files(log_dir,"original",llmfreq,"l4s")
    l4s_llm_logs = load_log_files(log_dir,"llm",llmfreq,"l4s")


    # print("original_logs",original_logs)
    # print("llm_logs",llm_logs)

    # print("----------------------------------------------")
    # print("Extracting data from original logs extract_data")
    # # Extract from original logs
    # steps_original, queue_delays_original, packet_lengths_original, losses_original = extract_data(original_logs)
    # print("----------------------------------------------")
    # print("Extracting data from LLM-enhanced logs extract_data")
    # # Extract from LLM-enhanced logs
    # steps_llm, queue_delays_llm, packet_lengths_llm, losses_llm = extract_data(llm_logs)

    print("----------------------------------------------")
    print("Extracting data from original logs extract_data_classic")
    # Extract from original logs    
    steps_classic_original, queue_delays_classic_original, packet_lengths_classic_original, losses_classic_original = extract_data_classic(classic_original_logs)
    print("----------------------------------------------")
    print("Extracting data from original logs extract_data_l4s")
    # Extract from original logs
    steps_l4s_original, queue_delays_l4s_original, packet_lengths_l4s_original, losses_l4s_original = extract_data_l4s(l4s_original_logs)

    # Extract from LLM-enhanced logs
    print("----------------------------------------------")
    print("Extracting data from LLM-enhanced logs extract_data_classic")
    # Extract from LLM-enhanced logs
    steps_classic_llm, queue_delays_classic_llm, packet_lengths_classic_llm, losses_classic_llm = extract_data_classic(classic_llm_logs)
    print("----------------------------------------------")
    print("Extracting data from LLM-enhanced logs extract_data_l4s" )
    # Extract from LLM-enhanced logs
    steps_l4s_llm, queue_delays_l4s_llm, packet_lengths_l4s_llm, losses_l4s_llm = extract_data_l4s(l4s_llm_logs)

        # Create DataFrame
    df, cdf_df = create_dataframe(steps_l4s_original, queue_delays_l4s_original, packet_lengths_l4s_original, losses_l4s_original,
                            steps_l4s_llm, queue_delays_l4s_llm, packet_lengths_l4s_llm, losses_l4s_llm)
    
    eval_tag = f"{llm_tag}_eval_{llmfreq}_freq_L4S"

    #         # Create DataFrame
    # df, cdf_df = create_dataframe(steps_classic_original, queue_delays_classic_original, packet_lengths_classic_original, losses_classic_original,
    #                         steps_classic_llm, queue_delays_classic_llm, packet_lengths_classic_llm, losses_classic_llm)
    
    # eval_tag = f"{llm_tag}_eval_{llmfreq}_freq_classic"

    # Add a tag to the folder for better organization
    tagged_folder = os.path.join(GRAPH_SAVE_FOLDER, eval_tag)

    # Ensure the tagged folder exists
    os.makedirs(tagged_folder, exist_ok=True)




    # Plot queue delay comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Step Number',
        ylabel='Queue Delay (s)',
        title=f'Queue Delay Comparison: Traditional vs {llm_tag}',
        filename=f"{eval_tag}_queue_delay_comparison",
        folder=tagged_folder
    )

    # Plot queue delay box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        ylabel='Queue Delay (s)',
        title=f'Queue Delay Comparison (Box Plot): Traditional vs {llm_tag}',
        filename=f"{eval_tag}_queue_delay_box_comparison",
        folder=tagged_folder
    )



    # Plot throughput comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Packet Length', 'LLM Packet Length'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Step Number',
        ylabel='Packet Length (Mbit)',
        title=f'Packet Length Comparison: Traditional vs {llm_tag}',
        filename=f"{eval_tag}_pkt_len_comparison",
        folder=tagged_folder
    )

    # Plot throughput box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Packet Length', 'LLM Packet Length'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        ylabel='Packet Length (Mbit)',
        title=f'Packet Length Comparison (Box Plot): Traditional vs {llm_tag}',
        filename=f"{eval_tag}_box_pkt_len_comparison",
        folder=tagged_folder
    )

    # Plot throughput comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Step Number',
        ylabel='Bandwidth Utilisation (Mbit/s)',
        title=f'Throughput Comparison: Traditional vs {llm_tag}',
        filename=f"{eval_tag}_throughput_comparison",
        folder=tagged_folder
    )

    # Plot throughput box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        ylabel='Bandwidth Utilisation (Mbit/s)',
        title=f'Bandwidth Utilisation Comparison (Box Plot): Traditional vs {llm_tag}',
        filename=f"{eval_tag}_throughput_box_comparison",
        folder=tagged_folder
    )



    # Plot throughput CDF comparison
    cdf_plot_line_comparison(
        cdf_df,
        index_rows='Original Throughput Sorted',
        columns=['Original Throughput CDF', 'LLM Throughput CDF'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
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
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Queue Delay (s)',
        ylabel='CDF',
        title='Queue Delay CDF Comparison',
        filename=f"{eval_tag}_queue_delay_cdf_comparison",
        folder=tagged_folder
    )


    df, cdf_df = create_dataframe(steps_classic_original, queue_delays_classic_original, packet_lengths_classic_original, losses_classic_original,
                            steps_classic_llm, queue_delays_classic_llm, packet_lengths_classic_llm, losses_classic_llm)
    
    eval_tag = f"{llm_tag}_eval_{llmfreq}_freq_classic"

    #         # Create DataFrame
    # df, cdf_df = create_dataframe(steps_classic_original, queue_delays_classic_original, packet_lengths_classic_original, losses_classic_original,
    #                         steps_classic_llm, queue_delays_classic_llm, packet_lengths_classic_llm, losses_classic_llm)
    
    # eval_tag = f"{llm_tag}_eval_{llmfreq}_freq_classic"

    # Add a tag to the folder for better organization
    tagged_folder = os.path.join(GRAPH_SAVE_FOLDER, eval_tag)

    # Ensure the tagged folder exists
    os.makedirs(tagged_folder, exist_ok=True)




    # Plot queue delay comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Step Number',
        ylabel='Queue Delay (s)',
        title=f'Queue Delay Comparison: Traditional vs {llm_tag}',
        filename=f"{eval_tag}_queue_delay_comparison",
        folder=tagged_folder
    )

    # Plot queue delay box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Queue Delay', 'LLM Queue Delay'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        ylabel='Queue Delay (s)',
        title=f'Queue Delay Comparison (Box Plot): Traditional vs {llm_tag}',
        filename=f"{eval_tag}_queue_delay_box_comparison",
        folder=tagged_folder
    )



    # Plot throughput comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Packet Length', 'LLM Packet Length'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Step Number',
        ylabel='Packet Length (Mbit)',
        title=f'Packet Length Comparison: Traditional vs {llm_tag}',
        filename=f"{eval_tag}_pkt_len_comparison",
        folder=tagged_folder
    )

    # Plot throughput box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Packet Length', 'LLM Packet Length'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        ylabel='Packet Length (Mbit)',
        title=f'Packet Length Comparison (Box Plot): Traditional vs {llm_tag}',
        filename=f"{eval_tag}_box_pkt_len_comparison",
        folder=tagged_folder
    )

    # Plot throughput comparison using the updated line plot function
    plot_line_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Step Number',
        ylabel='Bandwidth Utilisation (Mbit/s)',
        title=f'Throughput Comparison: Traditional vs {llm_tag}',
        filename=f"{eval_tag}_throughput_comparison",
        folder=tagged_folder
    )

    # Plot throughput box plot comparison using the updated box plot function
    plot_box_comparison(
        df,
        columns=['Original Throughput', 'LLM Throughput'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        ylabel='Bandwidth Utilisation (Mbit/s)',
        title=f'Bandwidth Utilisation Comparison (Box Plot): Traditional vs {llm_tag}',
        filename=f"{eval_tag}_throughput_box_comparison",
        folder=tagged_folder
    )



    # Plot throughput CDF comparison
    cdf_plot_line_comparison(
        cdf_df,
        index_rows='Original Throughput Sorted',
        columns=['Original Throughput CDF', 'LLM Throughput CDF'],
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
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
        labels=['Traditional DUALPI2', 'DUALPI2-LLM'],
        xlabel='Queue Delay (s)',
        ylabel='CDF',
        title='Queue Delay CDF Comparison',
        filename=f"{eval_tag}_queue_delay_cdf_comparison",
        folder=tagged_folder
    )