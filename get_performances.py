import requests
import time
import csv
import sqlite3

connection = sqlite3.connect('matches.db')
cursor = connection.cursor()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Accept-Language": "en,es-419;q=0.9,es;q=0.8",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": "RGAPI-f2dedee0-ecea-430a-bfc0-bcbf7b44a5cc"
}

with open("matches2.txt", "r") as file:

    for line in file:
        time.sleep(1)
        values = line.strip().split(",")
        match_id = values[1]
        request_url = f'https://americas.api.riotgames.com/lol/match/v5/matches/{match_id}'
        response = requests.get(request_url, headers=headers)
        
        if response.status_code != 200:
            print('{} Request error. HTTP code {}'.format(time.strftime("%Y-%m-%d %H:%M"), response.status_code))
            time.sleep(60)
            continue

        try:
            print("Request succesful")
            data = response.json()
            game_duration = data["info"]["gameDuration"]
            for participant in data["info"]["participants"]:
                summoner_id = participant["summonerId"]
                cursor.execute('SELECT rank FROM summoners WHERE summonerid = ?', (summoner_id,))
                result = cursor.fetchone()

                # Check if a result was found
                if result:
                    rank = result[0]
                    #print(f"The rank for summoner ID {summoner_id} is {rank}")
                else:
                    rank='UNRANKED'
                    #print(f"No rank found for summoner ID {summoner_id}")

                if "challenges" in participant:
                    challenge_team_baron_kills = participant["challenges"].get("teamBaronKills", "null")
                    challenge_kill_participation = participant["challenges"].get("killParticipation", "null")
                    challenge_team_rift_herald_kills = participant["challenges"].get("teamRiftHeraldKills", "null")
                    challenge_turret_plates_taken = participant["challenges"].get("turretPlatesTaken", "null")
                    challenge_lane_minions_first_10_minutes = participant["challenges"].get("laneMinionsFirst10Minutes", "null")
                else:
                    # Set null values for all challenges fields
                    challenge_team_baron_kills = "null"
                    challenge_kill_participation = "null"
                    challenge_team_rift_herald_kills = "null"
                    challenge_turret_plates_taken = "null"
                    challenge_lane_minions_first_10_minutes = "null"
                player_info = [
                    str(rank),
                    str(participant["puuid"]),
                    str(summoner_id),
                    str(game_duration),
                    str(participant["assists"]),
                    str(challenge_team_baron_kills),
                    str(challenge_kill_participation),
                    str(challenge_team_rift_herald_kills),
                    str(challenge_turret_plates_taken),
                    str(challenge_lane_minions_first_10_minutes),
                    str(participant["champExperience"]),
                    str(participant["champLevel"]),
                    str(participant["damageDealtToBuildings"]),
                    str(participant["damageDealtToObjectives"]),
                    str(participant["damageDealtToTurrets"]),
                    str(participant["deaths"]),
                    str(participant["detectorWardsPlaced"]),
                    str(participant["firstBloodAssist"]),
                    str(participant["firstBloodKill"]),
                    str(participant["firstTowerAssist"]),
                    str(participant["firstTowerKill"]),
                    str(participant["gameEndedInEarlySurrender"]),
                    str(participant["gameEndedInSurrender"]),
                    str(participant["goldEarned"]),
                    str(participant["kills"]),
                    str(participant["teamPosition"]),
                    str(participant["totalDamageDealt"]),
                    str(participant["totalDamageDealtToChampions"]),
                    str(participant["totalDamageTaken"]),
                    str(participant["totalMinionsKilled"]),
                    str(participant["turretsLost"]),
                    str(participant["wardsKilled"]),
                    str(participant["wardsPlaced"]),
                    str(participant["wardsKilled"]),
                    str(participant["totalDamageTaken"]),
                    str(participant["visionScore"]),
                    str(participant["allInPings"]),
                    str(participant["assistMePings"]),
                    str(participant["baitPings"]),
                    str(participant["basicPings"]),
                    str(participant["commandPings"]),
                    str(participant["dangerPings"]),
                    str(participant["enemyMissingPings"]),
                    str(participant["enemyVisionPings"]),
                    str(participant["holdPings"]),
                    str(participant["getBackPings"]),
                    str(participant["needVisionPings"]),
                    str(participant["onMyWayPings"]),
                    str(participant["pushPings"]),
                    str(participant["visionClearedPings"]),
                    str(participant["win"])
                ]
                with open("performances.txt", 'a') as file:
                    file.write(",".join(player_info))
                    file.write("\n")

        except Exception as e:
            print("ERROR:", e)
            with open("errors.txt", 'a') as error:
                error.write("ERROR in match:", match_id, "Exception:", e)

        print(f"Finished writing performances of match: {values[0]}, ID: {match_id}")

print("Finished nicely")
connection.close()