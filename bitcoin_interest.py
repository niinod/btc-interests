import pandas as pd
import numpy as np
import os

from forex_python.bitcoin import BtcConverter
b = BtcConverter()

from settings import local_currency, csv_directory


# Needed variables
pair = 'BTC/' + local_currency

# Exchangespecific functions for parsing csv-files.
def import_blockfi(file):
    global df

    df_file = pd.read_csv(file)

    df_file['Exchange'] = 'Blockfi'
    df_file.rename(columns={'Cryptocurrency': 'Coin',
                            'Transaction Type': 'Type',
                            'Confirmed At': 'Datetime'},
                   inplace=True)
    df_file = df_file[['Exchange','Coin','Amount','Type','Datetime']]
    df = pd.concat([df, df_file])

def import_celsius(file):
    global df

    df_file = pd.read_csv(file)

    df_file['Exchange'] = 'Celsius'
    df_file.rename(columns={' Date and time': 'Datetime',
                            ' Transaction type': 'Type',
                            ' Coin type': 'Coin',
                            ' Coin amount': 'Amount'},
                   inplace=True)
    df_file = df_file[['Exchange','Coin','Amount','Type','Datetime']]
    df = pd.concat([df, df_file])

def import_nexo(file):
    global df

    df_file = pd.read_csv(file)

    df_file['Exchange'] = 'Nexo'
    df_file.rename(columns={'Date / Time': 'Datetime',
                            'Currency': 'Coin'},
                  inplace=True)
    df_file = df_file[['Exchange','Coin','Amount','Type','Datetime']]
    df = pd.concat([df, df_file])

# Import all csv-files and create df with all interest payments.

df = pd.DataFrame(columns=['Exchange','Coin','Amount','Type','Datetime'])

csv_files = []
for path, dirs, files in os.walk(csv_directory):
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(path, file))

for file in csv_files:
    if 'blockfi' in file:
        print('Parsing %s' % file)
        import_blockfi(file)
    elif 'celsius' in file:
        print('Parsing %s' % file)
        import_celsius(file)
    elif 'nexo' in file:
        print('Parsing %s' % file)
        import_nexo(file)
    else:
        print('Unknown fileformat found: %s' % file)

print('Cleaning up data...')
df['Datetime'] = pd.to_datetime(df['Datetime'])
df = df.sort_values('Datetime')

df = df.replace(['FixedTermInterest', 'Interest Payment', 'interest'], 'Interest')
df = df[df['Type'] == 'Interest']

df.reset_index(drop=True, inplace=True)

df[pair] = np.nan
df[local_currency] = np.nan

# Calculate value of btc in local_currency on date for payment.
print('Calculating BTC price and %s value for all interest payments...' % local_currency)
for i in range(len(df)):
    try:
        df.at[i, local_currency] = b.convert_btc_to_cur_on(df.iloc[i]['Amount'], local_currency, df.loc[i]['Datetime'])
        df.at[i, pair] = b.get_previous_price(local_currency, df.loc[i]['Datetime'])
    except:
        print('Something wrong with index "%s"' % i)
        pass

df.at[i + 1, 'Exchange'] = 'Sum'
df.at[i + 1, local_currency] = df[local_currency].sum()
df.at[i + 1, 'Amount'] = df['Amount'].sum()

print('Exporting all payments to excel spreadsheet..')
df.to_excel('total_interest.xlsx', index=False)
print('Done!')