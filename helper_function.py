from datetime import datetime
from fetch_data import nba_stats
import matplotlib.pyplot as plt

# Function: get_season_year()
# Purpose: Handle user input and validation for the season year based on whether it's for player stats or team rankings
# Precondition: None
# Postcondition: Returns a valid season year string (e.g., '2024-25')
def get_season_year(is_for_player_stats=True):
    while True:
        season_id = input("Enter the season year (e.g., 2024-25): ")

        #validate season_id format
        if len(season_id) == 7 and season_id[:4].isdigit() and season_id[5:].isdigit():
            # extract starts year and end year from season_id
            start_year = int(season_id[:4]) # extract the start year from season (YYYY)
            end_year = int(season_id[5:]) # extract end year from season (YY)

            # adjust based on whether it's for player stats or team rankings
            if is_for_player_stats:
                # validate and retrieve the season year specifically for player stats (1996-current)
                if 1996 <= start_year <= datetime.now().year and end_year == (start_year % 100 + 1) % 100:
                    return season_id # return the valid season_id
                else:
                    print("Season year must be between 1996 and the current year with one year difference (e.g. 2024-25).\n")
            else:
                # validate and retrieve the season year specifically for team rankings (1970-current)
                if 1970 <= start_year <= datetime.now().year and end_year == (start_year % 100 + 1) % 100:
                    return season_id # return the valid season id for team rankings else:
                else:
                    print("Season year must be between 1970 and the current year with one year difference (e.g. 2024-25).\n")
        else:
            # error check for season_id format
            print("Incorrect season year format. Please use YYYY-YY format.\n")

# Function: get_season_type()
# Purpose: Handle user input and validation for the NBA season type (Regular Season or Playoffs)
# Precondition: None
# Postcondition: Returns a valid season type string 
def get_season_type():
    while True:
        season_type = input("Enter the season type (Regular Season/Playoffs): ")

        # validate if the input is correct
        if season_type not in ['Regular Season', 'Playoffs']:
            print("Incorrect format for season type. Please enter 'Regular Season' or 'Playoffs'.\n")
        else:
            return season_type

# Function: stats_data_exist()
# Purpose: Ensure that valid stats data is available for a given season ID and type
# Precondition: A season ID and season type must be provided
# Postcondition: If valid data is found, it returns the season ID and type; otherwise, prompts for new inputs
def stats_data_exist(id, types):
    while True:
        # create an instance of the nba_stats class with the given season ID and type
        nba_data = nba_stats(id, types.replace(" ", "%20"))
        
        stats_df = nba_data.get_stats() # fetch player stats from the API

        # check if there no data is available
        if stats_df.empty:
            print(f"No valid data available for the {id} {types}. Enter another again\n")

            # get new inputs
            id = get_season_year(is_for_player_stats=True)
            types = get_season_type()

        else: 
            return id, types # return if the data is not empty
         
# Function: top_players()
# Purpose: Retrieve the top 5 players based on a specific stat (PTS, AST, REB, STL, BLK) from NBA data
# Precondition: Valid 'nba data' object and a stat column
# Postcondition: Returns a DataFrame containing player names and the specified stat
def top_players(stat, nba_data):
    stats_df = nba_data.get_stats() # retrieve all the player stats
    return stats_df.sort_values(by = stat, ascending = False).head(5)[['PLAYER_NAME', stat]]

# Function: plot_stats()
# Purpose: Compare stats of two players with the top 5 players in specific categories
# Precondition: Valid 'nba_data' object and player names existing in the data
# Postcondition: Generates and saves a bar plot as 'compare_player_plot.png'
def plot_stats(first_name, second_name, first_nba_data, second_nba_data):
    # Define the stat categories and their column names 
    labels = ["Points", "Assists", "Rebounds", "Steals", "Blocks"] 
    column_stats = ["PTS", "AST", "REB", "STL", "BLK"]

    # fetch the stats for the two players
    first_stats_df = first_nba_data.get_stats() 
    second_stats_df = second_nba_data.get_stats()

    # will get the stats for top 5 players from the 2024-25 Regular Season
    nba_data = nba_stats('2024-25', 'Regular%20Season')

    # select the stats for the two players
    first_player_stats = first_stats_df[first_stats_df['PLAYER_NAME'] == first_name]
    second_player_stats = second_stats_df[second_stats_df['PLAYER_NAME'] == second_name]

    # values for the first and second player
    first_player_values = [
        first_player_stats["PTS"],
        first_player_stats["AST"],
        first_player_stats["REB"],
        first_player_stats["STL"],
        first_player_stats["BLK"]
    ]

    second_player_values = [
        second_player_stats["PTS"],
        second_player_stats["AST"], 
        second_player_stats["REB"],
        second_player_stats["STL"],
        second_player_stats["BLK"]
    ]

    # create a figure with subplots for each stat category 
    fig, axs = plt.subplots(1, 5, figsize = (18, 6)) # One subplot for each stat category

    # iterate through each stat category
    for i, stat in enumerate(column_stats): 
        ax = axs[i]

        # get the top 5 players and their stats
        top_5 = top_players(stat, nba_data)
        top_5_names = top_5["PLAYER_NAME"].tolist()
        top_5_values = top_5[stat].tolist()

        # plot the top 5 players
        ax.bar(range(5), top_5_values, width = 0.3, color = ["red", "orange", "yellow", "purple", "pink"], label = "Top 5 Players")

        # plot the first player's value
        ax.bar(5, first_player_values[i], width = 0.3, color = "blue", label = first_name)

        # plot the second player's value
        ax.bar(6, second_player_values[i], width = 0.3, color = "green", label = second_name)

        # customize the plot
        ax.set_xticks(range(7))
        ax.set_xticklabels(top_5_names + [first_name, second_name], rotation = 45, ha = 'right')
        ax.set_title(labels[i])
        ax.set_ylabel("Stat Value")

    # add a title to the whole figure
    fig.suptitle(f"Comparison of {first_name} and {second_name} against the Top 5 Players from the 2024-25 Regular Season", fontsize = 16)
    plt.tight_layout()

    # save the plot as a PNG image
    plt.savefig('compare_player_plot.png')