import requests
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_table
from utils.settings import NCOV19_API, REVERSE_STATES_MAP
from app import cache
import pandas as pd


def stats_table(state="US"):
    """Callback to change between news and twitter feed
    """
    state = REVERSE_STATES_MAP[state]
    # print(f'stats_table state is {state}')
    URL = NCOV19_API + "county"
    try:
        response = requests.get(URL)
    except:
        data = {"state_name": "john", "county_name": "cena", "confirmed":0, "death":0}
    
    if response.status_code == 200:        
        data = response.json()["message"]
        data = pd.DataFrame.from_records(data)
    else:
        data = {"state_name": "john", "county_name": "cena", "confirmed":0, "death":0}
    
    if state in ["US", "United States"]:
        data = data.groupby(["state_name"])["confirmed", "death"].sum()
        
        data = data.sort_values(by=['confirmed'], ascending=False)
        data = data.reset_index()
        data = data.rename(columns={"state_name": "State/County", 
                                    "confirmed": "Confirmed",
                                    "death": "Deaths"})
    else:
        data = data[data['state_name'] == state]
        data = data[["county_name", "confirmed", "death"]]
        data = data.sort_values(by=['confirmed'], ascending=False)
        data = data.rename(columns={"county_name": "State/County", 
                                    "confirmed": "Confirmed",
                                    "death": "Deaths"})                

    del response

    return data