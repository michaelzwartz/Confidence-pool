
import numpy as np


#function to combine picks and point values
def combine(df1):
    my_file = df1.copy()
    rows = my_file.shape[0]
    i = 2 
    while i < rows:
        for col in my_file.loc[:, my_file.columns != 'Game']:
            my_file[col][i+1] = float(my_file[col][i+1])
            my_file[col][i] = [my_file[col][i], my_file[col][i+1]]
        i = i+2
    
    my_file.drop([5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33, 35, 37, 39, 41], axis=0, inplace=True)
    return my_file

#function to calculate totals
def totals(df):
    max_score = 0
    games = len(df.columns)-1
    points = 16
    while games > 0:
        max_score = max_score + points
        points = points - 1
        games = games - 1
    i = 4  
    df['Score'] = 0
    df['Game Count'] = 0
    df['Max Score'] = max_score
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
    dog_spread_tot = 0
    big_dog_count = 0
    for col in df.loc[:, ~df.columns.isin(['Game', 'Score', 'Max Score'])]:
        if df[col][3] < 0 and df[col][1] == df[col][0]: #if home team is favorite and away team won
            upset_count = upset_count + 1
            dog_spread_tot = dog_spread_tot + -(df[col][3])
            print('Road upset alert ', df[col][0], "spread ", -(df[col][3]))
            if abs(df[col][3]) > 6.5:
                big_dog_count = big_dog_count + 1
                print("big dog woof woof")
        elif df[col][3] > 0 and df[col][2][0] == df[col][0]: #if away team is favorite and home team won
            upset_count = upset_count + 1
            dog_spread_tot = dog_spread_tot + df[col][3]
            print('Home dog win ', df[col][2])
            if abs(df[col][3]) > 6.5:
                big_dog_count = big_dog_count + 1
                print("big dog woof woof")
        elif df[col][0] == "TIE":
            tie_count = tie_count + 1
            print("A friggen tie...  ", df[col][2])
        else:
            fav_count = fav_count + 1
    
    dog_spread_avg = round(dog_spread_tot/upset_count, 2)
    print("Total of ", upset_count, "upsets this week. With ", big_dog_count, "being big dogs." )
    return upset_count, dog_spread_avg, big_dog_count #fav_count, tie_count

#number of total picks for league
def week_pick_percent(week_raw, week_game_total):
    games = len(week_raw.axes[1])-(week_raw.iloc[0].isna().sum() + 1)
    enteries = (len(week_raw.axes[0])-4)/2
    total_picks = games * enteries
    pick_percent = round(week_game_total/total_picks*100, 2)
    
    return pick_percent 

#finds avg points per win for league
def points_per_win (df):
    total_wins = df['Game Count'].sum()
    total_points = df['Score'].sum()
    avg_pts_per_win = total_points/total_wins
    points = round(avg_pts_per_win, 2)
    return points

#sum total points each week
def sum_totals(season_totals, week_stats, week_number_rank):
    season_totals[['Score', 'Game Count']] = season_totals[['Score', 'Game Count']] + week_stats[['Score', 'Game Count']]
    season_totals[week_number_rank] = season_totals['Score'].rank(ascending=False, method='min')

    return season_totals
