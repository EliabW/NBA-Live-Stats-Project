import socket
import sys
from helper_function import *

# Function: display_menu()
# Purpose: Display the main menu options for the NBA Live Stats
# Precondition: None
# Postcondition: Prints a list of option for user to choose from
def display_menu():
    print("\n=== Welcome to NBA Live Stats! ===")
    print("Please select an option:")
    print("1. View Player Stats")
    print("2. Compare Player Stats")
    print("3. View Games")
    print("4. View Team Rankings")
    print("5. Add New Record")
    print("6. Exit")
    print("====================================\n")

def main():
    # Get host and port from command line arguments
    if len(sys.argv) != 3: 
        print("Usage: python client.py <host> <port>")
        sys.exit(1)

    host = sys.argv[1] # host address (e.g., 'localhost') 
    port = int(sys.argv[2]) # port (e.g., 30005)

    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server 
    client_socket.connect((host, port))
    

    while True:
        display_menu() # display options for the user
        choice = input("Enter your choice (1-6): ")

        # send the choice to the server 
        client_socket.send(choice.encode())  
       
        if choice == "1":  # View Player Stats
            print("\nYou selected: View Player Stats")

            # Gather additional inputs for the player stats request
            season_year = get_season_year(is_for_player_stats = True)
            season_type = get_season_type()

            season_year, season_type = stats_data_exist(season_year, season_type) # make sure that the data is available 

            player_name = input("Enter the player's full name (First Last): ")

            # Send season year, season type, and player name to the server 
            client_socket.send(f"{season_year},{season_type},{player_name}".encode())

            while True:
                #Receive and print the response from the server
                response = client_socket.recv(8000).decode() 
                print(f"\n=== Message from server ===\n{response}\n")

                # check for error
                if "No stats found" in response:
                    player_name = input("Enter the player's full name (First Last): ")
                    client_socket.send(f"{season_year},{season_type},{player_name}".encode()) 
                else:
                    break # exit the loop if successful

        elif choice == "2": # Compare Player Stats
            print("\nYou selected: Compare Player Stats")
            print("Enter detail for first player stats")

            # get valid inputs for season year and type of first player
            first_season_year = get_season_year(is_for_player_stats=True) # set it true if we are getting player stats
            first_season_type = get_season_type()

            first_season_year, first_season_type = stats_data_exist(first_season_year, first_season_type) # make sure that the data is available 

            # get the name of first player
            first_player_name= input("Enter the player's full name (First Last): ")

            # send the user inputs to the server
            client_socket.send(f"{first_season_year},{first_season_type},{first_player_name}".encode())

            while True:
                # recieve message from the server
                first_response = client_socket.recv(8000).decode()

                # check for error
                if "No stats found" in first_response:
                    print(f"\n=== Message from server ===\n{first_response}\n")

                    # get the name of first player and send it to the server again
                    first_player_name= input("Enter the player's full name (First Last): ")
                    client_socket.send(f"{first_season_year},{first_season_type},{first_player_name}".encode())
                else:
                    print(f"\n=== Message from server ===\n{first_response}\n") 
                    break # exit the loop if successful


            print("\nEnter detail for second player stats")
            # get vald inputs for season year and season type of second player
            second_season_year = get_season_year(is_for_player_stats = True) # set it true if getting player stats
            second_season_type = get_season_type()

            second_season_year, second_season_type = stats_data_exist(second_season_year, second_season_type) # make sure that the data is available 

            # get the name of second player
            second_player_name= input("Enter the player's full name (First Last): ")

            # send the user inputs to the server
            client_socket.send(f"{second_season_year},{second_season_type},{second_player_name}".encode())

            while True:
                # recieve message from the server
                second_response = client_socket.recv(8000).decode()

                # check for error
                if "No stats found" in second_response:
                    print(f"\n=== Message from server ===\n{second_response}\n")

                    # get the name of second player and send it to the server again
                    second_player_name= input("Enter the player's full name (First Last): ")
                    client_socket.send(f"{second_season_year},{second_season_type},{second_player_name}".encode())
                else:
                    print(f"\n=== Message from server ===\n{second_response}\n") 
                    break # exit the loop if successful

            # receieve comparison result from the server
            comparison_result = client_socket.recv(8000).decode()
            print(f"\n=== Message from server ===\n{comparison_result}\n") 

        elif choice == "3": # View Games
            print("\nYou selected: View Games")

            # get the game date and send it to the server
            game_date = input("Enter the game date in YYYYMMDD format: ")
            client_socket.send(game_date.encode())

            while True:
                # receive the message from the server and display it
                response = client_socket.recv(8000).decode()
                print(f"\n=== Message from server ===\n{response}\n")

                # check for error
                if "Check the date format" in response or "Do not have record" in response or "Invalid date format" in response:
                    # ask and send the date again
                    game_date = input("Enter the game date in YYYYMMDD format: ")
                    client_socket.send(game_date.encode())
                else:
                    break # exit the loop if successful

        elif choice == "4": # View Team Rankings
            print("\n You selected: View Team Rankings")

            # get the season year and send it to server
            season_id = get_season_year(is_for_player_stats=False) # set to False if getting team ranking
            client_socket.send(season_id.encode())

            # receieve and display message from the server
            response = client_socket.recv(8000).decode()
            print(f"\n=== Message from server ===\n{response}\n")

        elif choice == "5": # add new record
            print("\nYou selected: Add New Record")

            while True:
                # get the username and password and send them to the server
                admin_username = input("Enter admin username: ")
                admin_password = input("Enter admin password: ")
                client_socket.send(f"{admin_username},{admin_password}".encode())

                # receieve message from the server
                response = client_socket.recv(8000).decode()

                # check if sucessful
                if response == "Login successful":
                    print(f"\n=== Message from server ===\n {response}\n")
                    break # exit the loop

                else:
                    print(f"\n=== Message from server ===\n{response}\n")
                    continue # ask again
                    

            while True:
                print("What kind of record would you like to add?")
                print("1. Add Player Stats")
                print("2. Cancel")

                # get the user input choice and send it to the server
                record_choice = input("Enter your choice (1-2): ")
                client_socket.send(record_choice.encode())


                if record_choice == '1': # add player stats
                    # ask user relevant stats and send them to the server
                    player_name = input("Enter the player's full name (First Last): ")
                    points = input("Enter the points scored: ")
                    assists = input("Enter the assists made: ")
                    rebounds = input("Enter the rebounds grabbed: ")
                    client_socket.send(f"{player_name},{points},{assists},{rebounds}".encode())

                    # receive message from the server and display it
                    response = client_socket.recv(8000).decode()
                    print(f"\n=== Message from server ===\n{response}\n")

                elif record_choice == '2': # cancel
                    # recieve response from server 
                    response = client_socket.recv(8000).decode() 
                    print(f"\n=== Message from server ===\n {response}\n")

                    break # exit the loop

                else:
                    print("\nInvalid choice, select between 1 and 2.\n")

        elif choice == "6": # Exit
            # recieve message from server and display it 
            response = client_socket.recv(8000).decode()
            print(f"\n=== Message from server ===\n{response}\n")

            break # exit the main loop

        else:
            # invalid option
            response = client_socket.recv(8000).decode()
            print(f"\n=== Message from server ===\n{response}\n")

    # close the connection
    client_socket.close()

if __name__ == "__main__":
    main()