from pathlib import Path

import pandas as pd

# Set the pandas display options to display all columns
pd.set_option('display.max_columns', None)

def describe_dataframe(df):
    """ Description of the contents of the data using Pandas dataframe functions.

            Read the data from the file and perform the following operations:
            - Display the first 5 rows of the dataframe
            - Display the shape of the dataframe
            - Display the column names
            - Display the data types of the columns
            - Display summary statistics
            - Display any missing values in the dataframe

            Parameters:
            data_file (Path): Filepath of the file in csv or excel format
    """
    #Display the shape of the dataframe
    print(df.shape)

    #Display the first 5 rows of the dataframe
    print(df.head())

    #Print the column names
    print(df.columns)

    #Print column data types
    print(df.dtypes)

    #Print information about the dataframe 
    print(df.info())

    #Describe the dataframe
    print(df.describe())

    #Display any missing values in the dataframe
    print(df[df.isna().any(axis=1)])

    # Print columns with missing values
    print("\nColumns with missing values:")
    print(df.isnull().sum())

def prepare_dataframe(df_raw, df_npc=None):
    """ Prepare the data for analysis by performing the following operations:
            - Drop rows with missing values
    """

    # Drop rows with missing values
    df_raw = df_raw.drop(index=[0,17,31])
    df_raw = df_raw.reset_index(drop=True)

    # Convert a specific column from float64 to int
    float_columns = df_raw.select_dtypes(include=['float64']).columns
    for col in float_columns:
        df_raw[col] = df_raw[col].astype('int')

    #print("\nData types of all columns after conversion:")
    #print(df.dtypes)

    # Convert a specific column from object to datetime
    df_raw['start'] = pd.to_datetime(df_raw['start'], format='%d/%m/%Y')
    df_raw['end'] = pd.to_datetime(df_raw['end'], format='%d/%m/%Y')

    #print("\nData types of all columns after conversion:")
    #print(df.loc[:, ['start', 'end']].dtypes)
    #print(df.dtypes)

    replacement_names = {
        'UK': 'Great Britain',
        'USA': 'United States of America',
        'Korea': 'Republic of Korea',
        'Russia': 'Russian Federation',
        'China': "People's Republic of China"
    }

    # Replace names in the 'country' column using the dictionary
    df_raw['country'] = df_raw['country'].replace(replacement_names)

    #Merge the two datasets
    if df_npc is not None:
        merged_df = pd.merge(df_raw, df_npc, how='left', left_on='country', right_on='Name')

    #Drop columns that are not needed for analysis
    df_prepared = merged_df.drop(columns=['URL', 'disabilities_included', 'highlights', 'Name'], axis=1)
    #print(df_prepared.head())

    #Insert a new column, 'duration' that calculates the duration of the event
    insert_loc = df_prepared.columns.get_loc('end') #0
    duration = (df_prepared['end'] - df_prepared['start']).dt.days.astype(int)
    df_prepared.insert(insert_loc + 1, 'duration', duration)
    print(df_prepared.head())

    #Save the prepared dataframe to a new file
    filepath_to_save = Path(__file__).parent.parent.joinpath('data', 'paralympics_events_prepared.csv')
    df_prepared.to_csv(filepath_to_save, index=False)

if __name__ == '__main__':
    paralympics_datafile_csv = Path(__file__).parent.parent.joinpath('data', 'paralympics_events_raw.csv')

    paralympics_datafile_excel = Path(__file__).parent.parent.joinpath('data', 'paralympics_all_raw.xlsx')

    npc_csv = Path(__file__).parent.parent.joinpath("data", "npc_codes.csv")

    # Read the data from the files into a Pandas dataframe. Includes error handling for the file read
    try:
        events_csv_df = pd.read_csv(paralympics_datafile_csv)
    except FileNotFoundError as e:
        print(f"File not found. Please check the file path. Error: {e}")

    events_excel_df = pd.read_excel(paralympics_datafile_excel)
    medal_standings_df = pd.read_excel(paralympics_datafile_excel, sheet_name="medal_standings")
    df_npc = pd.read_csv(npc_csv, usecols=['Code', 'Name'], encoding='utf-8', encoding_errors='ignore')

    # Strip whitespace from all values in the 'type' column
    events_csv_df['type'] = events_csv_df['type'].str.strip()

    #Make all values in the 'type' column lowercase
    events_csv_df['type'] = events_csv_df['type'].str.lower()
    
    prepare_dataframe(events_csv_df, df_npc)
    # Call the function to describe the dataframe
    #describe_dataframe(events_csv_df)
    #describe_dataframe(events_excel_df)
    #describe_dataframe(medal_standings_df)

    # Call function to prepare the dataframe
    #prepare_dataframe(events_csv_df)
    #prepare_dataframe(events_csv_df, df_npc)