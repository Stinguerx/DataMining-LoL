import requests
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en,es-419;q=0.9,es;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-ed5031e9-45d6-446c-aa47-355ab323baac"
}

tiers = ['IRON', 'BRONZE', 'SILVER', 'GOLD', 'PLATINUM', 'EMERALD', 'DIAMOND']
divisions = ['I','II','III','IV']
leagues = ['masterleagues', 'grandmasterleagues', 'challengerleagues']

for tier in leagues:
    for division in divisions:
        total_ids = 0
        print("Requesting tier", tier, "division", division)
        for page in range(1,1000):
            time.sleep(1)
            request_url = 'https://la2.api.riotgames.com/lol/league/v4/entries/RANKED_SOLO_5x5/{}/{}?page={}'.format(tier, division, page)
            #URL for master, grandmaster, challenger
            #request_url = 'https://la2.api.riotgames.com/lol/league/v4/{}/by-queue/RANKED_SOLO_5x5/'.format(tier)
            response = requests.get(request_url, headers=headers)
            if response.status_code != 200:
                print('{} Request error. HTTP code {}'.format(time.strftime("%Y-%m-%d %H:%M"), response.status_code))
                break
            
            try:
                data = response.json().get("entries")
                
                if data == []:
                    print("Reached end of pages:", page)
                    break
                
                else:
                    summoner_ids = [entry["summonerId"] for entry in data]
                    total_ids += len(summoner_ids)
                    #print(f"Found {len(summoner_ids)} summoner_ids in page {page}")
                    with open("summoner_ids.txt", "a") as file:
                        for summoner_id in summoner_ids:
                            file.write(tier[:-7].upper() + "," + summoner_id + "\n")
            
            except Exception as e:
                print("Error decoding")
            
        print(f"{total_ids} SummonerIds extracted from TIER {tier} DIVISION {division} and saved to summoner_ids.txt")






