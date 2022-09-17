import pandas as pd
import numpy as np
import os.path

out_file = "Week-1-Results.txt"

print("Calculating the scores...")

week1_raw = pd.read_csv("Pool_results.csv")

#function to combine picks and bets
def combine(df1):
    my_file = df1
    rows = my_file.shape[0]
    i = 2 
    while i < rows:
        for col in my_file.loc[:, my_file.columns != 'Name']:
            my_file[col][i+1] = float(my_file[col][i+1])
            my_file[col][i] = [my_file[col][i], my_file[col][i+1]]
        i = i+2
    return my_file

#function to count upsets, favoites, ties
def upset_counter(df):
    upset_count = 0
    fav_count = 0
    tie_count = 0
    for col in week1.loc[:, ~week1.columns.isin(['Name', 'Score'])]:
        if week1[col][3] < 0 and week1[col][1] == week1[col][0]: #if away team is favorite and home team won
            upset_count = upset_count + 1
        elif week1[col][3] > 0 and week1[col][2][0] == week1[col][0]: #if home team is favorite and away team won
            upset_count = upset_count + 1
        elif week1[col][0] == "TIE":
            tie_count = tie_count + 1
        else:
            fav_count = fav_count + 1
    
    return upset_count, fav_count, tie_count

#function to calculate total points
def totals(df):
    i = 4
    df['Score'] = 0
    while i < 42:
        for col in df.loc[:, ~df.columns.isin(['Name', 'Score'])]:
            if df[col][0] == df[col][i][0]:
                df['Score'][i] = df['Score'][i] + df[col][i][1]
        i = i + 2
    return df


week1 = combine(week1_raw)
week1.drop([3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43], axis=0, inplace=True)
week1 = totals(week1)

upset_count_wk1 = upset_counter(week1)[0]
fav_count_wk1 = upset_counter(week1)[1]
tie_count_wk1 = upset_counter(week1)[2]

#print scores in txt file (must be a string, not a df)
#f=open(out_file, "w+")
#f.write(week1[['Name', 'Score']])
#f.close()