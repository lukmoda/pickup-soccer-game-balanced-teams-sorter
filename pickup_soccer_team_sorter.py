import pandas as pd
import numpy as np
import random

def find_teams(guess):
    indexes_team1 = [i for i, e in enumerate(guess) if e == 1]
    indexes_team2 = [i for i, e in enumerate(guess) if e == 2]
    indexes_team3 = [i for i, e in enumerate(guess) if e == 3]
    indexes_team4 = [i for i, e in enumerate(guess) if e == 4]

    team1 = df.loc[indexes_team1]
    team2 = df.loc[indexes_team2]
    team3 = df.loc[indexes_team3] 
    team4 = df.loc[indexes_team4]

    avgs = [x["rating"].mean() for x in [team1, team2, team3, team4]]
    max_diff = max(avgs) - min(avgs)
    return team1, team2, team3, team4, max_diff

def print_teams(time1, time2, time3, time4, max_diff):
    for x in [time1, time2, time3, time4]:
        x["aux"] = x["player"] + " (" + x["rating"].astype(str) + ")"
        
    print('Team 1: ', time1.aux.values)
    print('Team 2: ', time2.aux.values)
    print('Team 3: ', time3.aux.values)
    print('Team 4: ', time4.aux.values)
    
    print('\nAverage team 1: {:.2f}'.format(time1['rating'].mean()))
    print('Average team 2: {:.2f}'.format(time2['rating'].mean()))
    print('Average team 3: {:.2f}'.format(time3['rating'].mean()))
    print('Average team 4: {:.2f}'.format(time4['rating'].mean()))
    
    print('Diff best vs worst team: {:.2f}'.format(max_diff))

df = pd.read_csv('PlayersRatings.csv')

df = df.loc[df['is_going'] == 1]
groups = [df for _, df in df.groupby('rating')]
random.shuffle(groups)

df = pd.concat(groups).reset_index(drop=True)
df = df.sort_values(by='rating', ascending=False).reset_index(drop=True)

initial_guess = [1,2,3,4,4,3,2,1,1,2,3,4,4,3,2,1,1,2,3,4]
team1, team2, team3, team4, max_diff = find_teams(initial_guess)

print('Initial Solution: \n')
print_teams(team1, team2, team3, team4, max_diff)

new_guess = initial_guess.copy()
best_guess = initial_guess.copy()
max_diff_best = max_diff.copy()
max_diff_list = [max_diff]
max_trials = 10000
count = 0
while count < max_trials and max_diff_best > 0:
    random.shuffle(new_guess)
    _, _, _, _, max_diff = find_teams(new_guess)
    max_diff_list.append(max_diff)
    if max_diff < max_diff_best:
        max_diff_best = max_diff
        best_guess = new_guess.copy()
    count += 1
    
#pd.DataFrame({"data": max_diff_list}).plot(kind='hist')

print('\nOptimized Solution: \n')
team1_best, team2_best, team3_best, team4_best, max_diff_best = find_teams(best_guess)
print_teams(team1_best, team2_best, team3_best, team4_best, max_diff_best)