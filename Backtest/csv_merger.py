import os
import pandas as pd
import math
from pathlib import Path

#LOOP THROUGH ALL CSV FILES IN FOLDER
#folder="C:\Users\Renaldo.Moonu\Desktop\folder name"
#for file in Path(folder).glob('*.csv'):

csv_folder = 'D:/Desktop Backup/School/Homework/Statistics/Python Stuff/Backtest/Results/SPSS Regression Files - Phase Two/'
num_tracker = 1
first_file = csv_folder + f'trading_summary_win_1.001_loss_0.9_time_0_period_2021-04-11_2019-01-01_versi_1.csv'
csvs = [fille for fille in Path(csv_folder).glob('*.csv')]

begin_exit_win = 1.001
end_exit_win = 1.1

begin_exit_loss = 0.85
end_exit_loss = 1.0

# for x in range(0,11):
#     incr = x * 0.01
#     perc = begin_exit_win + incr
#     perc = round(perc, 4)
#     for y in range(0,16):
#         incry = y * 0.01
#         percy = begin_exit_loss + incry
#         percy = round(percy, 4)
#         filename = csv_folder + f'trading_summary_win_{perc}_loss_{percy}_time_{percy}_period_2021-03-26_2019-01-01_vers_1.csv'
#         if filename not in csvs:
#             csvs.append(filename)
#         else:
#             pass


df1 = pd.read_csv(first_file, header=1, index_col=0)

# df1.drop('Annual Return (%)')
# df1 = df1.iloc[1:]
df1 = df1.drop(df1.iloc[:, 0:7], axis=1)
df1 = df1.drop('Annual Return (%)', axis=1)
df1 = df1.dropna()
sums = [math.sqrt((df1['Win Rate'][i])**2 + (df1['Profit (%)'][i])**2) for i in range(0, len(df1))]
df1['Sum of Squares'] = sums
df = df1

print(len(csvs))
for i in range(len(csvs)):
    df2 = pd.read_csv(csvs[i], header=1, index_col=0)

    df2 = df2.drop(df2.iloc[:, 0:7], axis=1)
    df2 = df2.drop('Annual Return (%)', axis=1)
    df2 = df2.dropna()
    sums = [math.sqrt((df2['Win Rate'][i])**2 + (df2['Profit (%)'][i])**2) for i in range(0, len(df2))]
    df2['Sum of Squares'] = sums

    df = df.append(df2)
    df = df.reset_index(drop=True)
df = df.sort_values('Sum of Squares', ascending=False)
print(df)
# oldf = pd.read_csv('SPSS.csv', header=0)
# df = oldf.append(df)
# print(oldf)
df.to_csv('SPSS_test.csv', index=False)