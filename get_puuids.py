import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en,es-419;q=0.9,es;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-ed5031e9-45d6-446c-aa47-355ab323baac"
}

category_counts = {}

with open("summoner_ids.txt", "r") as file, open("puuids_capped2.txt", 'a') as file2:
    previous = "None"
    count = 0
    while True:
        line = file.readline()
        if not line:
            break
        values = line.strip().split(',')
        rank = values[0]
        if rank not in category_counts:
            category_counts[rank] = 0
        
        if category_counts[rank] < 600:
            time.sleep(1)
            request_url = 'https://la2.api.riotgames.com/lol/summoner/v4/summoners/{}'.format(values[1])
            response = requests.get(request_url, headers=headers)
            if response.status_code != 200:
                print('{} Request error. HTTP code {}'.format(time.strftime("%Y-%m-%d %H:%M"), response.status_code))
                continue
            try:
                print("Request succesful")
                data = response.json()
                file2.write(values[0] + "," + values[1] + "," + data["puuid"] + "\n")
                category_counts[rank] += 1
                print(category_counts)
            
            except Exception as e:
                print("Error")

    print("Finished processing")  
        