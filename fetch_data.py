import requests
import pandas as pd
from datetime import datetime

# Class: nba_stats
# Purpose: Fetch and process NBA player statistics for a given season and season type
class nba_stats:
    # Function: __init__()
    # Purpose: Initialize the nba stats class with the specified season ID and season type
    # Precondition: Valid season ID and season type must be provided (default: 2024-25 Regular Season)
    # Postcondition: Sets up the URL and request headers required to fetch NBA player statistics
    def __init__(self, season_id='2024-25', season_type='Regular%20Season'):
        self.season_id = season_id
        self.season_type = season_type
        self.info_url = f'https://stats.nba.com/stats/leaguedashplayerstats?College=&Conference=&Country=&DateFrom=&DateTo=&Division=&DraftPick=&DraftYear=&GameScope=&GameSegment=&Height=&ISTRound=&LastNGames=0&LeagueID=00&Location=&MeasureType=Base&Month=0&OpponentTeamID=0&Outcome=&PORound=0&PaceAdjust=N&PerMode=PerGame&Period=0&PlayerExperience=&PlayerPosition=&PlusMinus=N&Rank=N&Season={season_id}&SeasonSegment=&SeasonType={season_type}&ShotClockRange=&StarterBench=&TeamID=0&VsConference=&VsDivision=&Weight='

        self.headers = {
            'x-nba-stats-token': 'true',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    # Function: fetch_data()
    # Purpose: Fetch raw player statistics data from the NBA API
    # Precondition: The URL and headers must be correctly configured
    # Postcondition: Returns the JSON response containing player statistics
    def fetch_data(self):
        response = requests.get(url = self.info_url, headers = self.headers).json()
        return response
    
    # Function: get_stats()
    # Purpose: Extract and format key player statistics into a pandas DataFrame
    # Precondition: Data must be fetched successfully using fetch_data()
    # Postcondition: Returns a DataFrame with selected columns (e.g., PLAYER_NAME, AST, REB, PTS)
    def get_stats(self):
        data = self.fetch_data()

        # match column names from the NBA API
        columns_list = ['PLAYER_NAME', 'AST', 'REB', 'STL', 'BLK', 'PTS']

        player_info = data['resultSets'][0]['rowSet']

        df = pd.DataFrame(player_info, columns = data['resultSets'][0]['headers'])

        return df[columns_list]

# Class: nba_ranking
# Purpose: Retrieve and display team rankings for the NBA regular season
class nba_ranking:
    # Function: __init__()
    # Purpose: Initialize the nba ranking class with a specified season ID
    # Precondition: A valid season ID must be provided (default: 2024-25 Regular Season)
    # Postcondition: Sets up the URL and headers required to fetch team rankings
    def __init__(self, season_id = '2024-25'):
        self.season_id = season_id
        self.info_url = f'https://stats.nba.com/stats/leaguestandingsv3?GroupBy=conf&LeagueID=00&Season={season_id}&SeasonType=Regular%20Season&Section=overall'

        self.headers = {
            'referer': 'https://www.nba.com/',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        }

    # Function: fetch_data()
    # Purpose: Fetch raw player statistics data from the NBA API
    # Precondition: The URL and headers must be correctly configured
    # Postcondition: Returns the JSON response containing team rankings data
    def fetch_data(self):
        response = requests.get(url = self.info_url, headers = self.headers).json()
        return response
    
    # Function: get_ranking()
    # Purpose: Extract and format key team rankings data into a pandas DataFrame
    # Precondition: Data must be fetched successfully using fetch_data()
    # Postcondition: Returns a DataFrame with selected columns (e.g., TeamName. WINS, LOSSES)
    def get_ranking(self):
        data = self.fetch_data()

        # match column names from the NBA API
        columns_list = ['TeamName', 'WINS', 'LOSSES', 'ConferenceRecord', 'Conference']

        team_info = data['resultSets'][0]['rowSet'] # get the data

        df = pd.DataFrame(team_info, columns = data['resultSets'][0]['headers'])

        return df[columns_list]
    

# Class: nba_scoreboard
# Purpose: Retrieve and display the scoreboard of recent NBA games for a given date
class nba_scoreboard:
    # Function: __init__()
    # Purpose: Initialize the nba scoreboard class with a specified game_date
    # Precondition: A valid game date in the format 'YYYYMMDD' must be provided
    # Postcondition: Sets up the URL for fetching NBA game scores
    def __init__(self,game_date):
        self.game_date = game_date
        self.info_url = f'https://api.foxsports.com/bifrost/v1/nba/league/scores-segment/{game_date}?apikey=jE7yBJVRNAwdDesMgTzTXUUSx1It41Fq'

    # Function: format date()
    # Purpose: Convert a date string in 'YYYYMMDD' format to 'MM-DD-YYYY.
    # Precondition: A valid date string in 'YYYYMMDD' format must be provided.
    # Postcondition: Returns the formatted date string
    def format_date(self, date):
        convert_date = datetime.strptime(date, '%Y%m%d')
        return convert_date.strftime('%m-%d-%Y')

    # Function: fetch_data()
    # Purpose: Fetch raw player statistics data from the foxsports API
    # Precondition: The URL and headers must be correctly configured
    # Postcondition: Returns the JSON response containing scoreboard data
    def fetch_data(self):
        response = requests.get(url = self.info_url).json()
        return response
    
    # Function: get_event_detail()
    # Purpose: Safely retrieve a specific key value from an event dictionary
    # Precondition: A valid event dictionary and key must be provided
    # Postcondition: Returns the value for the specified key or a default value if the key is missing
    def get_event_detail(self, event, key, default_value = 'Not available'):
        return event.get(key, default_value)

    # Function: extract_scoreboard_info()
    # Purpose: Extract and format detailed information about games played on the given date
    # Precondition: Data must be fetched successfully using fetch_data()
    # Postcondition: Returns a string summary of all game events for the date
    def extract_scoreboard_info(self):
        data = self.fetch_data()

        events = data['sectionList'][0]['events']

        result_messages = []  # concatenate to display the game events
        
        # proccess all the event
        for event in events:
            # get the home team and away with their game status
            home_team = event['upperTeam']['longName']
            away_team = event['lowerTeam']['longName']
            game_status = self.get_event_detail(event, 'statusLine')
            headline = self.get_event_detail(event, 'eventHeadline', 'No headline available')

            result_messages.append(f'Headline: {headline}') # add event headline

            # check if the game is FINAL or done 
            if game_status == 'FINAL':
                home_score = event['upperTeam']['score']
                away_score = event['lowerTeam']['score']

                # add message that shows the game result
                result_messages.append(f'{home_team} vs {away_team} on {self.format_date(self.game_date)} where the {game_status} score is {home_score} - {away_score}\n')
            else:
                # the message will be game that will happen in the future
                result_messages.append(f'{home_team} vs {away_team} on {self.format_date(self.game_date)}\n')

        # add a new line for the list of appended messages for clarity 
        return '\n'.join(result_messages)