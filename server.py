from fetch_data import *
from helper_function import *
import socket
import sys
import threading

# Function: player_stats()
# Purpose: Retrieve and display statistics for a specific player during a given season
# Precondition: A valid season ID, season type, and player name must be provided
# Postcondition: Returns player stats if available; otherwise, an error message is returned
def player_stats(season_id, season_type, player_name):
    # create an instance of the nba_stats class
    nba_data = nba_stats(season_id, season_type.replace(" ", "%20"))

    # fetch player stats
    stats_df = nba_data.get_stats()

    # check if the player exists in the DataFrame
    if player_name in stats_df['PLAYER_NAME'].values:
        # get the stats associated to the player name
        player_stats_df = stats_df[stats_df['PLAYER_NAME'] == player_name]
        return f"Stats for {player_name}:\n{player_stats_df.to_string()}" # return if successful
    else:
        # return an error message 
        return f"No stats found for player: {player_name}"
    
# Function: get_team_rank()
# Purpose: Fetch and display team rankings for a given NBA season
# Precondition: A valid season ID must be provided
# Postcondition: Returns a DataFrame with team rankings for the specified season
def get_team_rank(season_id):
    nba_data = nba_ranking(season_id) # create an instance of nba_ranking with the specified

    rankings_df = nba_data.get_ranking() # fetch the team rankings

    # display the entire column of the df and return it
    return f"\nTeam Rankings for the Season:\n{rankings_df.to_string()}\n"

# Function: get_games()
# Purpose: Retrieve game scores and details for a specific date
# Precondition: A valid game date in YYYYMMDD format must be provided
# Postcondition: Returns a summary of game results for the given date or an error message
def get_games(game_date):
    # check if game data follow the correct format and length
    if len(game_date) == 8 and game_date.isdigit():
        try:
            datetime.strptime(game_date, "%Y%m%d") # ensure that the game date is a valid calender date

            # call the class to access the scoreboard of games 
            nba_data = nba_scoreboard(game_date)

            # get news of the games from fox sport API
            response = nba_data.extract_scoreboard_info()

            # check if there are no news
            if not response:
                return f"Do not have record of the game found for {nba_data.format_date(game_date)}. Either there is no information about the game yet in the API or that the date was before the records started since 10-17-2017.\n"

            return response # if successful, returns the formated news

        # catch invalid calender dates (e.g. Feb 30)
        except ValueError:  
            return "Invalid date format. Please use YYYYMMDD format."
    else:
        return "Check the date format. Please use YYYYMMDD format.\n"


# Function: compare_player_stats()
# Purpose: Compare stats of players
# Precondition: Valid season years, types, and player names for both players must be provided 
# Postcondition: A plot comparing stats of both plauyers against the top 5 players is generated and saved as a PNG file
def compare_player_stats(first_season_year, first_season_type, first_player_name, second_season_year, second_season_type, second_player_name):
    # get the data of first and second player stats from user inputs
    first_player_data = nba_stats(first_season_year, first_season_type.replace(" ", "%20"))
    second_player_data = nba_stats(second_season_year, second_season_type.replace(" ", "%20"))

    # generate the plot and save it
    plot_stats(first_player_name, second_player_name, first_player_data, second_player_data)



# Function: add_record()
# Purpose: Add a new player's stats to the 'stats_record.csv file
# Precondition: Player name, points, assists, and rebounds must be provided
# Postcondition: Saves the player's stats to the CSV file and returns a confirmation message
def add_record(player_name, points, assists, rebounds): 
    # write in stats_record.csv with the given name, points, assists, and rebounds
    with open('stats_record.csv', mode='a', newline='') as file:
        file.write(f" {player_name}, {points}, {assists}, {rebounds}\n") 

    return f"New player stats added to stats_record.csv: {player_name} - Points: {points}, Assists: {assists}, Rebounds: {rebounds}"

# Function: server_function()
# Purpose: Handle client requests for NBA stats-related options and process them on the server side
# Precondition: A connected client_socket must be provided alongside the client_address
# Postcondition: Responds to client requests, processes user input, and sends results back to the client
def server_function(client_socket, client_address):
    host = "localhost"
    while True:
        # receive the option selected by the client 
        choice = client_socket.recv(8000).decode()

        if choice == "1": # View Player Stats
            # receive season year, season type, and player name from the client 
            player_info = client_socket.recv(8000).decode()
            season_year, season_type, player_name = player_info.split(',')

            # get the player stats or error messages if not found 
            response = player_stats(season_year, season_type, player_name)

            # send the response to the client
            client_socket.send(response.encode())

            # check if no stats were found and prompt for a new player name 
            while "No stats found" in response:
                # get the new player name response from client
                player_info = client_socket.recv(8000).decode()
                season_year, season_type, player_name = player_info.split(',')

                # send the response back to the client again
                response = player_stats(season_year, season_type, player_name)
                client_socket.send(response.encode())

        elif choice == "2": # Compare Player Stats
            # recive client message about first player info
            first_player_data = client_socket.recv(8000).decode()

            # send response back to the client 
            first_season_year, first_season_type, first_player_name = first_player_data.split(',') 
            first_response = player_stats(first_season_year, first_season_type, first_player_name)
            client_socket.send(first_response.encode())

            # check for error first player until valid
            while "No stats found" in first_response:
                # get another message from client
                first_player_data = client_socket.recv(8000).decode()

                # send the response again 
                first_season_year, first_season_type, first_player_name = first_player_data.split(',')
                first_response = player_stats(first_season_year, first_season_type, first_player_name)
                client_socket.send(first_response.encode())

            # recive client message about second player info
            second_player_data = client_socket.recv(8000).decode()

            # send response back to the client 
            second_season_year, second_season_type, second_player_name = second_player_data.split(',')
            second_response = player_stats(second_season_year, second_season_type, second_player_name)
            client_socket.send(second_response.encode())

            # check error for second player until valid
            while "No stats found" in second_response:
                # get another message from client
                second_player_data = client_socket.recv(8000).decode()

                # send the response again 
                second_season_year, second_season_type, second_player_name = second_player_data.split(',')
                second_response = player_stats(second_season_year, second_season_type, second_player_name)
                client_socket.send(second_response.encode())

            # use user inputs that was sent from the client to perform comparison and generate plot
            comparison_result = compare_player_stats(first_season_year, first_season_type, first_player_name, second_season_year, second_season_type, second_player_name)

            # send the messsage back to the client
            client_socket.send("Comparison plot has been saved successfully as a PNG image".encode())

        elif choice == "3": # View Recent Games
            # get the message from client about game date
            game_date = client_socket.recv(8000).decode()

            # send response back to the client
            response = get_games(game_date)
            client_socket.send(response.encode())

            # check for error until valid
            while "Check the date format" in response or "Do not have record" in response or "Invalid date format" in response:
                # get the message from client about game date
                game_date = client_socket.recv(8000).decode()

                # send response back to the client
                response = get_games(game_date)
                client_socket.send(response.encode())

            
        elif choice == "4": # View Team Rankings
            # get message from client about the season year
            season_year = client_socket.recv(8000).decode()
            
            # send response back to client
            response = get_team_rank(season_year)
            client_socket.send(response.encode())

        elif choice == "5": # Add New Record
            # continue until valid user and password

            while True:
                # get response from client about username and password
                admin_credentials = client_socket.recv(8000).decode()
                admin_username, admin_password = admin_credentials.split(',')

                # if valid
                if admin_username == "admin_user" and admin_password == "admin_pass":
                    client_socket.send("Login successful".encode()) # send successful messsage to client
                    break # exit the code

                else:
                    client_socket.send("Invalid admin credentials, try again".encode()) # send error message to client

            while True:
                # get choice option from the client
                choice = client_socket.recv(8000).decode()

                if choice == "1":
                    # get the stats info from the client
                    stats_recieve = client_socket.recv(8000).decode()

                    # send the response back to the client
                    player_name, points, assists, rebounds = stats_recieve.split(',') 
                    response = add_record(player_name, points, assists, rebounds)
                    client_socket.send(response.encode())

                elif choice == "2":
                    client_socket.send("Cancelled. Returning to the main menu".encode()) # send exit message back to client
                    break # exit the code

                else:
                    client_socket.send("Invalid choice. Please try again.".encode()) # send an invalid option back to client

        elif choice == "6": # Exit
            # send response back to client
            client_socket.send("Exiting the program. Bye!".encode())
            break # exit from the loop

        else:
            # invalid option
            client_socket.send("Invalid option, select between 1-6".encode())

    # close the connection
    client_socket.close()
    print(f"(localhost, {client_address[1]}) disconnected")

def main():
    # get the port from command line argument
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    host = "localhost" 
    port = int(sys.argv[1]) # port passed as command line argument

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # create a socket object

    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # reuse adress to avoid error

    server_socket.bind((host, port)) # bind the socket to the host and port 

    # start listening for incoming connections
    server_socket.listen(5) # allow up to 5 clients to wait in the queue

    # accept connection from the client
    while True:
        try:
            client_socket, client_address = server_socket.accept()

            print(f"Connected to ({host}, {client_address[1]})") 

            # create a new thread for the client
            client_thread = threading.Thread(target = server_function, args = (client_socket, client_address))

            client_thread.start()

        # user can press Ctrl+C without KeyboardInterrupt error displayed after user choose option 6 to exit
        except KeyboardInterrupt:
            print() # make new line for visual
            break 
            
if __name__ == "__main__":
    main()