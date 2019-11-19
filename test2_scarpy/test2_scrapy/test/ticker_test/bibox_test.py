import requests



data = requests.get('https://api.bibox.com/v1/mdata?cmd=marketAll', timeout=15).json()

print(data)