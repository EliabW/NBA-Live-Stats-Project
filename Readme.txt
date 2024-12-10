I ran my code using JuypterHub 

Set up Instruction:
    1. Download these files onto JuypterHub: 
        - client.py 
        - server.py
        - helper_function.py
        - fetch_data.py 

    2. Go to the terminal on JuypterHub, and you you need to install these packages to run the code:
        - pip install requests
        - pip install pandas
        - pip install matplotlib

How to run the code:
    1. Start the server
        - In the terminal, run this command: python server.py 3240
            - You can replace 3240 with any port values between 0-65535

    2. Start the client 
        - Go to a separate terminal, and run this: python client.py localhost 3240
            - make sure that port value (3240) matches the one one used in server command (for establishing a connection)

How to run the program:
    - After running the client program, you will see the main menu with a list of options to choose from and each option have an instruction to follow:
        1. View Player Stats: Gets individual player stats
        2. Compare Player Stats: Create a bar plot comparing the stats of the two inputted players alongside the top 5 player stats from 2024-25 Regular Season
        3. View Games: Displays game results and headlines based on the given date
        4. View Team Rankings: Displays team rankings based on the year
        5. Add New Record: Requires admin credentials (username and password) to add player name, points, assists, and rebound to csv file. You can also exit and return to the main menu
        6. Exit: End the program 

    - Here is a demo video on YouTube that goes in depth: https://youtu.be/_mogPYTlPVA

