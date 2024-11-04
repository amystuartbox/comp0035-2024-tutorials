import pandas as pd
import matplotlib.pyplot as plt 
from pathlib import Path

paralympics_prepared_csv = Path(__file__).parent.parent.joinpath('data', 'paralympics_events_prepared.csv')

# Read the data from the files into a Pandas dataframe. Includes error handling for the file read:
prepared_df = pd.read_csv(paralympics_prepared_csv)

#Draw an ERD for the data in the attached csv file.