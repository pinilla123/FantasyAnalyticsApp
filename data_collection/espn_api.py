import requests
import pandas as pd


# Get draft details
def get_draft_details(league_id, season_id, espn_cookies):
    headers = {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    }
    # url from the network tab
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}/segments/0/leagues/{league_id}?view=mDraftDetail&view=mSettings&view=mTeam&view=modular&view=mNav"
    # get request to espn
    r = requests.get(url, headers=headers, cookies=espn_cookies)
    # raw data in dictionary
    espn_raw_data = r.json()

    # we access the dictionary "draftDetail" and then we access the key "picks"
    # to access its associated value (array of picks, which are also dictionaries)
    # and we save that to "draft_picks"
    espn_draft_detail = espn_raw_data
    draft_picks = espn_draft_detail["draftDetail"]["picks"]

    # We create a data frame "df" using the list of dictionaries "draft_picks"
    # only want three columns so we specify by passing list of desired columns
    # and we do so with square brackets [ [list] ]
    df = pd.DataFrame(draft_picks)
    draft_df = df[["overallPickNumber", "playerId", "teamId"]]

    return draft_df


######################################################################


# Get player info
def get_player_details(season_id, espn_cookies):
    custom_headers = {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
        "X-Fantasy-Filter": '{"filterActive":null}',
        "X-Fantasy-Platform": "kona-PROD-b4d4346a62f06aac9356deafde4a4a15b9ed0676",
        "X-Fantasy-Source": "kona",
    }
    url = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}/players?scoringPeriodId=0&view=players_wl"
    # get request to espn
    r = requests.get(url, headers=custom_headers, cookies=espn_cookies)
    # raw data in dictionary
    player_data = r.json()
    df = pd.DataFrame(player_data)
    # only necessary columns for players
    player_df = df[["defaultPositionId", "fullName", "id", "proTeamId"]].copy()
    # rename id to avoid naming issues in our databases
    player_df.rename(columns={"id": "player_id"}, inplace=True)

    return player_df


######################################################################


def get_team_details(season_id, espn_cookies):
    headers = {
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    }
    # url from the network tab
    url = f"https://fantasy.espn.com/apis/v3/games/ffl/seasons/{season_id}?view=proTeamSchedules_wl"
    r = requests.get(url, headers=headers, cookies=espn_cookies)
    team_data = r.json()

    team_names = team_data["settings"]["proTeams"]
    df = pd.DataFrame(team_names)

    # get only necessary columns
    team_df = df[["id", "location", "name"]].copy()
    # add a column with full team name
    team_df["team_name"] = (
        team_df["location"].astype(str) + " " + team_df["name"].astype(str)
    )

    # rename in place
    team_df.rename(columns={"id": "team_id"}, inplace=True)
