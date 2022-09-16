import pandas as pd
import numpy as np
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

week1 = combine(week1_raw)
week1.drop([3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41, 43], axis=0, inplace=True)

#function to calculate total points
i = 4
week1['Score'] = 0
while i < 42:
    #print(i)
    for col in week1.loc[:, ~week1.columns.isin(['Name', 'Score'])]:
        if week1[col][0] == week1[col][i][0]:
            week1['Score'][i] = week1['Score'][i] + week1[col][i][1]
            #print(week1['Name'][i], ' the ', col, 'was a good game')
        #else:
            #print(week1['Name'][i], "haha, you suck")
    i = i + 2


week1[['Name', 'Score']]