import pandas as pd
import matplotlib.pyplot as plt 
from pathlib import Path



def view_distribution(df, columns=None):
    """Draw a histogram of specified columns in the DataFrame to visualise the distribution of the
    data.

    Parameters:
        df : pd.DataFrame   The DataFrame to plot
        columns : list      The column names to plot

    Returns:
        None
    """

    # Create a histogram of the DataFrame
    if columns:
        df[columns].hist()
    else:
        df.hist()

     # Show the plot
    plt.show()

def view_outliers(df):
    """Draw boxplot of the DataFrame columns to visualise the distribution of the data.

    Useful for identifying outliers.

    Each column is plotted into a separate subplot.

    Parameters:
        df : pd.DataFrame   The DataFrame to plot

    Returns:
        None
    """

    # Create a boxplot of the DataFrame
    df.plot.box(subplots=True, sharey=False)
    plt.savefig('bp_tutorial.png')
    plt.show()
 
def view_timeseries(df):
    """Draw a timeseries plot of the DataFrame using the specified date and value columns.

    Sort the rows in date order before plotting.

    Parameters:
        df : pd.DataFrame   The DataFrame to plot
        date_column : str   The column name containing the date data
        value_column : str  The column name containing the value data
        filter_value: str   The value to filter the DataFrame by

    """
    df = df.sort_values(by='start')
    
    # Sort the DataFrame by the date column
    df.plot(x='start', y='participants')
    plt.show()

if __name__ == "__main__":
    paralympics_prepared_csv = Path(__file__).parent.parent.joinpath('data', 'paralympics_events_prepared.csv')

    # Read the data from the files into a Pandas dataframe. Includes error handling for the file read
    try:
        prepared_df = pd.read_csv(paralympics_prepared_csv)
    except FileNotFoundError as e:
        print(f"File not found. Please check the file path. Error: {e}")

    #view_distribution(prepared_df, columns=['participants_m', 'participants_f'])

    #Create histograms for summer and winter events
    prepared_summer_df = prepared_df[prepared_df["type"] == "summer"]
    #view_distribution(prepared_summer_df)

    prepared_winter_df = prepared_df[prepared_df["type"] == "winter"]
    #view_distribution(prepared_winter_df)

    view_timeseries(prepared_df)
