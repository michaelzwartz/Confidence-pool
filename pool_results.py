import pandas as pd
import numpy as np

#function to combine picks and point values
def combine(df1):
    my_file = df1
    rows = my_file.shape[0]
    i = 2 
    while i < rows:
        for col in my_file.loc[:, my_file.columns != 'Game']:
            my_file[col][i+1] = float(my_file[col][i+1])
            my_file[col][i] = [my_file[col][i], my_file[col][i+1]]
        i = i+2
    
    df1.drop([5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41], axis=0, inplace=True)
    return my_file

#function to calculate totals
def totals(df):
    i = 4
    df['Score'] = 0
    df['Game Count'] = 0
    df['Max Score'] = 136
    while i < 41:
        for col in df.loc[:, ~df.columns.isin(['Game', 'Score', 'Game Count', 'Max Score'])]:
            if df[col][0] is np.nan:
                break
            
            elif df[col][0] == df[col][i][0]:
                df.loc[i, 'Game Count'] = df.loc[i, 'Game Count'] + 1
                df.loc[i, 'Score'] = df.loc[i, 'Score'] + df.loc[i, col][1]
            
            else:  
                df.loc[i, 'Max Score'] = df.loc[i, 'Max Score'] - df.loc[i, col][1]
               
        i = i + 2
    return df

#upset counter
def upset_counter(df):
    upset_count = 0
    fav_count = 0
    tie_count = 0
    for col in df.loc[:, ~df.columns.isin(['Game', 'Score', 'Max Score'])]:
        if df[col][3] < 0 and df[col][1] == df[col][0]: #if home team is favorite and away team won
            upset_count = upset_count + 1
            #print('Road upset alert ', df[col][0], "spread ", -(df[col][3]))
        elif df[col][3] > 0 and df[col][2][0] == df[col][0]: #if away team is favorite and home team won
            upset_count = upset_count + 1
            #print('Home dog win ', df[col][2])
        elif df[col][0] == "TIE":
            tie_count = tie_count + 1
            #print("A friggen tie...  ", df[col][2])
        else:
            fav_count = fav_count + 1
    print("Total of ", upset_count, "upsets this week")
    return upset_count, fav_count, tie_count