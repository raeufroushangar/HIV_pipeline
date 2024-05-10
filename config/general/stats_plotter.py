import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def plot_distribution(dataframe, column_name, plot_color, tick_interval=50, switch='yes', title='', xlabel='', ylabel=''):
    # Calculate mean and median
    mean_val = round(dataframe[column_name].mean(), 2)
    median_val = round(dataframe[column_name].median(), 2)

    # Calculate min and max length
    min_val = dataframe[column_name].min()
    max_val = dataframe[column_name].max()

    # Calculate starting and ending ticks
    starting_tick = tick_interval * (min_val // tick_interval) - tick_interval  # Start from the 100th base before min length
    ending_tick = tick_interval * (max_val // tick_interval) + tick_interval  # End at the 100th base after max length

    # Set bin edges from the starting tick to the ending tick with bin size specified by tick_interval
    bin_edges = np.arange(starting_tick, ending_tick + tick_interval, tick_interval)

    # Set a larger figure size for the plot
    plt.figure(figsize=(20, 8))

    # Plot the distribution with bins every specified tick interval
    ax = sns.histplot(dataframe[column_name], bins=bin_edges, color=plot_color, edgecolor='gray')
    plt.title(title, fontsize=10)
    plt.xlabel(xlabel, fontsize=9)
    plt.ylabel(ylabel, fontsize=9)

    # Add red dashed line for the mean
    plt.axvline(mean_val, color='red', linestyle='--', label=f'Mean: {mean_val}')

    # Add green dashed line for the median
    plt.axvline(median_val, color='darkgoldenrod', linestyle='--', label=f'Median: {median_val}')

    # Add small vertical lines for min and max
    plt.axvline(min_val, color='blue', linestyle='--', label=f'Min: {min_val}', ymin=0, ymax=0.05)
    plt.axvline(max_val, color='green', linestyle='--', label=f'Max: {max_val}', ymin=0, ymax=0.05)

    if switch.lower() == 'yes':
        # Calculate lowest and top 2.5% percentiles
        lowest_2p5_percentile = np.percentile(dataframe[column_name], 2.5)
        top_2p5_percentile = np.percentile(dataframe[column_name], 97.5)

        # Add vertical dashed lines for lowest and top 2.5%
        plt.axvline(lowest_2p5_percentile, color='brown', linestyle='--', label=f'Lowest 2.5%: {round(lowest_2p5_percentile, 2)}')
        plt.axvline(top_2p5_percentile, color='purple', linestyle='--', label=f'Top 2.5%: {round(top_2p5_percentile, 2)}')

    # Set x-ticks every specified tick interval with smaller font size and rotate them at 45 degrees
    plt.xticks(np.arange(starting_tick, ending_tick + tick_interval, tick_interval), fontsize=8, rotation=45)

    # Set y-ticks every 500 with smaller font size
    plt.yticks(np.arange(0, plt.gca().get_ylim()[1] + 500, 500), fontsize=8)

    # Show legend with smaller font size
    plt.legend(fontsize=8)

    # Add frequency labels on top of each bar
    for rect in ax.patches:
        height = rect.get_height()
        ax.annotate(f'{int(height)}', xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8)



def calculate_stats(dataframe, column_name):
    # Calculate mean and median
    mean = round(dataframe[column_name].mean(), 2)
    median = round(dataframe[column_name].median(), 2)

    # Count the number of sequences above, at, and below mean and median
    counts = {
        '> mean': (dataframe[column_name] > mean).sum(),
        '= mean': (dataframe[column_name] == mean).sum(),
        '< mean': (dataframe[column_name] < mean).sum(),
        '> median': (dataframe[column_name] > median).sum(),
        '= median': (dataframe[column_name] == median).sum(),
        '< median': (dataframe[column_name] < median).sum(),
    }

    # Calculate percentages
    total_counts = len(dataframe)
    percentages = {key: (value / total_counts * 100) for key, value in counts.items()}

    # Create a DataFrame for the percentages, then transpose it
    percentages_df = pd.DataFrame(list(percentages.items()), columns=['Sequences Length', 'Value (%)'])

    # Round the values to two decimal places
    percentages_df['Value (%)'] = percentages_df['Value (%)'].round(2)

    # Transpose the DataFrame
    transposed_df = percentages_df.T

    # Rename the columns of the transposed DataFrame for clarity
    transposed_df.columns = transposed_df.iloc[0] # Set new column headers
    transposed_df = transposed_df.drop(transposed_df.index[0]) # Drop the initial row now used as header

    return transposed_df


