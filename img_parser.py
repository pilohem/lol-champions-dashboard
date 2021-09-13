import requests
import json

f = open('data/lol_champion.json')
data = json.load(f)

available_champions = list(data['data'].keys())

# Define the remote file to retrieve
for champion in available_champions:
    print(champion)
    remote_url = f'http://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champion}_0.jpg'
    # Define the local filename to save data
    local_file = f'img/champion/{champion}_0.jpg'
    # Make http request for remote file data
    data = requests.get(remote_url)
    # Save file data to local copy
    with open(local_file, 'wb') as file:
        file.write(data.content)

