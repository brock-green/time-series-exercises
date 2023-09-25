import os
import pandas as pd
import requests
from env import host, user, password, create_url

def retrieve_swapi_data(data_type):
    '''
    Retrieve data from SWAPI and cache it to a local CSV file.

    Args:
        data_type (str): The type of data to retrieve ("people," "planets," or "starships").

    Returns:
        pd.DataFrame: A DataFrame containing the retrieved data.
    '''
    # Define the CSV file path
    csv_file_path = f'{data_type}_csv.csv'

    if os.path.isfile(csv_file_path):
        # If CSV file exists, read in data from the CSV file.
        data_df = pd.read_csv(csv_file_path, index_col=0)
    else:
        data_df = pd.DataFrame()
        api_url = f"https://swapi.dev/api/{data_type}/"
        next_page_url = api_url

        while next_page_url:
            # Make a GET request to the API
            response = requests.get(next_page_url)

            # Check if the request was successful
            if response.status_code == 200:
                # Convert the API response to a DataFrame
                page_data = response.json()
                data = page_data.get("results", [])

                if not data:
                    break  # Exit the loop if there are no more pages

                # Append the page data to the main DataFrame
                page_df = pd.DataFrame(data)
                data_df = pd.concat([data_df, page_df], ignore_index=True)

                # Get the URL of the next page if available
                next_page_url = page_data.get("next")
            else:
                print(f"Error: Unable to fetch data from SWAPI for {data_type}")
                break
        
        # Save the retrieved data to a CSV file
        data_df.to_csv(csv_file_path)

    return data_df


def get_starwars():
    '''
    for each people, planets, and starships; runs retrieve_swapi_data to acquire and cache data. Then concats the three df's into one starwars df. Returns df's for people, planets, starships, and combined starwars df.
    '''
    people = retrieve_swapi_data('people')
    planets = retrieve_swapi_data('planets')
    starships = retrieve_swapi_data('starships')
    
    starwars = pd.concat([people, planets, starships])
    
    return people, planets, starships, starwars

def get_german_power():
    '''
    reads in csv to dataframe. Returns dataframe.
    '''
    power = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    
    return power

def get_store_data():
    '''
    Checks to see if tsa_item_demand exists. If it does the csv is read in to a df. If not Codeup cloud server is accessed to retrieve data, then cached to csv.
    Returns a dataframe of all store data in the tsa_item_demand.
    '''
    
    if os.path.exists('tsa_store_data.csv'):
        df = pd.read_csv('tsa_store_data.csv')
        
    else:
          
        url = create_url('tsa_item_demand')

        query = '''
                SELECT *
                FROM items
                JOIN sales USING(item_id)
                JOIN stores USING(store_id)
                '''

        df = pd.read_sql(query, url)
        df.to_csv('tsa_store_data.csv', index=False)
    return df