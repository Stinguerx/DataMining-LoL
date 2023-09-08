import requests
import time
import sqlite3

connection = sqlite3.connect('matches.db')
cursor = connection.cursor()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en,es-419;q=0.9,es;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": ""
}

with open("puuids_true.txt", "r") as file:
    for line in file:
        values = line.strip().split(',')
        puuid = values[2]
        request_url = 'https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid/{}/ids?startTime=1689811200&type=ranked&start=0&count=100'.format(puuid)
        response = requests.get(request_url, headers=headers)
        if response.status_code != 200:
            print('{} Request error. HTTP code {}'.format(time.strftime("%Y-%m-%d %H:%M"), response.status_code))
            time.sleep(100)
            continue
        try:
            time.sleep(1)
            print("Request succesful")
            data = response.json()
            for match_id in data:
                cursor.execute('SELECT COUNT(*) FROM match WHERE match_id = ?', (match_id,))
                count = cursor.fetchone()[0]

                # If the match_id doesn't exist, insert it into the database
                if count == 0:
                    cursor.execute('INSERT INTO match (match_id) VALUES (?)', (match_id,))
                
            connection.commit()
            print("Successfully processed matches from Rank", values[0] ," PUUID:", puuid)
        except Exception as e:
            print("Error", e)
        

connection.close()
