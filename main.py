import profile as p

# Enter Summoner ID and server region even after driver starts
username = input("Enter summoner ID:")
server_region = input("Enter summoner region:")
player1 = p.Profile(username, server_region)

player1.open().search_player().extract_info().close()