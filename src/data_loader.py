import os
import pandas as pd

# --------------------------------------------------
# Get all CSV files from data folders
# --------------------------------------------------

def get_all_csv_files(base_path="data"):

    file_list = []

    for root, dirs, files in os.walk(base_path):

        for file in files:

            if file.endswith(".csv"):

                full_path = os.path.join(root, file)

                file_list.append(full_path)

    file_list.sort()

    print(f"Total CSV files found: {len(file_list)}")

    return file_list


# --------------------------------------------------
# Process one CSV file
# --------------------------------------------------

def process_single_file(file_path):

    try:

        df = pd.read_csv(file_path)

        # Filter NIFTY Futures
        df = df[df['Ticker'] == 'NIFTY-I.NFO'].copy()

        if df.empty:
            return None

        # Create Datetime column
        df['Datetime'] = pd.to_datetime(
            df['Date'] + ' ' + df['Time'],
            dayfirst=True,
            format='mixed'
        )

        # Set Datetime index
        df.set_index('Datetime', inplace=True)

        # Sort by time
        df.sort_index(inplace=True)

        return df

    except Exception as e:

        print(f"Error processing file: {file_path}")

        print(e)

        return None