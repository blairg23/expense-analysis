import pandas as pd
from glob import glob
import os

data_folder = 'data'
input_folder = os.path.join('..', data_folder, 'discover')
output_folder = input_folder
input_csv_filenames = os.path.join(input_folder, '*.csv')
output_csv_filename = os.path.join(output_folder, 'all_transactions.csv')


all_transactions_dataframe = None

with open(output_csv_filename,'a+') as out_file:
    for input_csv_filename in glob(input_csv_filenames):
        if input_csv_filename != output_csv_filename:
            print(f"Processing {input_csv_filename}...")
            input_csv_dataframe = pd.read_csv(input_csv_filename)
            # print(f"Input CSV DataFrame: {input_csv_dataframe}")
            if all_transactions_dataframe is None:
                all_transactions_dataframe = input_csv_dataframe
            else:
                all_transactions_dataframe = pd.concat([all_transactions_dataframe, input_csv_dataframe])

            # print(f"All Transactions DataFrame: {all_transactions_dataframe}")

all_transactions_dataframe['Post Date'] = pd.to_datetime(all_transactions_dataframe['Post Date'])
all_transactions_dataframe.sort_values('Post Date', ascending=True, inplace=True)
all_transactions_dataframe.to_csv(output_csv_filename, index=False)
