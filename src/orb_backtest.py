import pandas as pd

#Steps involved
# 1. Read all files under the folder one by one.
# 2. for every file, create new dataframe for Nifty futures only (index) - NIFTY-I.NFO
# 3. Sort with time ascending and inplace - index on time
# 4. Create another dataframe for options data - sort time (ascending) index on time
# 5. Create a method to select required strike on CE/PE side for current or next month
# 6. method to calculate ORB H/L


all_data = pd.read_csv("data/2023/GFDLNFO_BACKADJUSTED_27092023.csv")
# Filter Nifty Futures
filt = all_data['Ticker'] == 'NIFTY-I.NFO'
Nifty_data = all_data.loc[filt].copy()

# Combine Date + Time → Datetime
Nifty_data['Datetime'] = pd.to_datetime(
    Nifty_data['Date'] + ' ' + Nifty_data['Time'],
    format='%d/%m/%Y %H:%M:%S'
)

# Set index
Nifty_data.set_index('Datetime', inplace=True)

# Sort
Nifty_data.sort_index(inplace=True)

print(Nifty_data.head())

def orb_range(data, orb_minutes=15):
    """
    Calculate ORB High and Low

    Parameters:
    data : DataFrame
    orb_minutes : int
        Number of minutes for ORB window

    Returns:
    orb_high, orb_low
    """

    market_open = "09:15:00"

    # ORB end time
    orb_end = (
        pd.to_datetime(market_open)
        + pd.Timedelta(minutes=orb_minutes)
    ).time()

    # Select ORB window
    orb_window = data.between_time(
        market_open,
        orb_end.strftime("%H:%M:%S")
    )

    # Calculate ORB High & Low
    orb_high = orb_window['High'].max()
    orb_low = orb_window['Low'].min()

    return orb_high, orb_low

high, low = orb_range(Nifty_data, orb_minutes=15)

print("ORB High:", high)
print("ORB Low :", low)