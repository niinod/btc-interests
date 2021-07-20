# btc-interests

# Introduction:
A simple program that takes input of csv-files from Bitcoin lending services,
extracts every interest payout, and calculates the fiat value of the interest
payout, on the day of the payout.

The results comes in form of a excel-file with every interest payouy, value on
the day of the payout, sum of bitcoin paid out, and sum of fiat value.

These numbers can then be used if one need such numbers when reporting taxes.

Currently the program has been tested with csv-files from Blockfi, Celsius and
Nexo.

It will only work for Bitcoin. No shitcoins are supported.

# Installation
Install required packages from requirements.txt. Place csv from your lending
platform in one directory (Default is ./csv_files/, but can be chosen in
settings.py).

Edit 'settings.py' and set local currency.

Note: csv-files should be named: blockfi.csv, celsius.csv, nexo.csv.

# Contribute
I currently only have access to csv files from named platforms. Should you
need the program be able to parse files from other platforms as well, feel free
to send me a copy of the csv-file. (Remember to remove amounts.)

I also welcome all other input. This project is my first on Github, and its
mostly for my own learning experiance.

NOTE: If you download this, and find it usefull, please let me know :)