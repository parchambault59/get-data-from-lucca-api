from dotenv import load_dotenv
import requests
import pandas as pd
import json
import os
import sys

CONFIG_PATH = 'config.json'
API_KEY_VARIABLE_NAME = 'API_KEY'
ACCOUNT_VARIABLE_NAME = 'ACCOUNT_NAME'
SANDBOX_VARIABLE_NAME = 'SANDBOX_NAME'
OUTPUT_DIR = "outputs/"
CONTRACTS_INDEX = "1"
DEPARTMENTS_INDEX = "2"
EMPLOYEES_INDEX = "3"
EXIT_INDEX = "0"

def load_config(path):
    """
    Load configuration from a JSON file.
    Configuration file contains necessary information to build the API URL and parameters.

    Args:
        path (str): The file path to the JSON configuration file.

    Returns:
        dict: The configuration data loaded from the JSON file.
    """
    with open(path) as config_file:
        return json.load(config_file)
    
def load_from_dotenv(variable_name):
    """
    Load value of the specified environment variable from a .env file.

    Args:
        variable_name (str): The name of the environment variable to retrieve.

    Returns:
        str or None: The value of the environment variable if it exists, otherwise None.
    """
    load_dotenv()
    return os.getenv(variable_name)

def build_url(account_name, sandbox_name, config, data_type):
    """
    Constructs a URL based on the provided account, sandbox name, configuration, and data type.
    Args:
        account_name (str): The account name or identifier.
        sandbox_name (str): The sandbox environment name.
        config (dict): A dictionary containing configuration settings, including:
            - 'api_url_start' (str): The starting part of the API URL.
            - 'api_url_middle' (str): The middle part of the API URL.
            - '{data_type}_api_url_end' (str): The ending part of the API URL specific to the data type.
        data_type (str): The type of data for which the URL is being constructed.
    Returns:
        str: The constructed URL.
    """
    start = config['api_url_start']
    middle = config["api_url_middle"]
    end = config[f"{data_type}_api_url_end"]
    url = f"{start}{account_name}-{sandbox_name}{middle}{end}"
    return url

def get_params(config, data_type):
    """
    Generates a dictionary of parameters based on the provided configuration and data type.

    Args:
        config (dict): A dictionary containing configuration settings.
        data_type (str): The type of data for which parameters are being generated.

    Returns:
        dict: A dictionary containing the parameters for the specified data type.
    """
    base = config.get(f"{data_type}_params")
    params = {
        "fields": base
        }
    return params

def fetch_data(url, headers, params):
    """
    Fetches data from the API.
    
    Args:
        url (str): The API endpoint URL.
        headers (dict): The headers to include in the API request.
        params (dict): The parameters to include in the API request.
        
    Returns:
        dict: The JSON response from the API.
        
    Raises:
        requests.exceptions.RequestException: If an error occurs during the API request.
    """
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à l'API: {e}")
        return None
    
def process_employees_data(data):
    """
    Specific data processing for employees to address nested values issue.
    
    Args:
        data (dict): The raw data fetched from the API.
        
    Returns:
        pd.DataFrame: A DataFrame containing the processed employee data.
    """
    data = data.get('data', []).get('items', [])
    data = pd.DataFrame(data)
    data['departement_id'] = data['department'].apply(lambda x: x['id'])
    data['manager_id'] = data['manager'].apply(lambda x: x['id'] if x is not None else None).astype('Int64')
    data = data.drop(['department', 'manager'], axis=1)
    return data
    
def process_data(data, object_name):
    """
    Processes the given data based on the specified object name and returns a pandas DataFrame.
    Parameters:
    data (dict): The data to be processed. It should be a dictionary containing the relevant information.
    object_name (str): The type of object the data represents. It can be one of the following:
                       - "contracts": Processes contract data.
                       - "departments": Processes department data.
                       - "employees": Processes employee data.
    Returns:
    pd.DataFrame: A pandas DataFrame containing the processed data. If no data is found, returns None.
    """
    if not data:
        print("Aucun contrat trouvé.")
        return None
    if object_name == "contracts":
        data = data.get('items', [])
    elif object_name == "departments":
        data = data.get('data', []).get('items', [])
    elif object_name == "employees":
        data = process_employees_data(data)
    return pd.DataFrame(data)
    
def get_data(api_key, config, data_type):
    """
    Intermediate function that orchestrates the fetching and processing of data from the API based on the specified data type.
    Args:
        api_key (str): The API key for authentication.
        config (dict): Dictionnary containing necessary information to build the API URL and parameters.
        data_type (str): The type of data to fetch (e.g., 'employees').
    Returns:
        dict: The processed data retrieved from the API.
    Raises:
        KeyError: If the data_type is not found in the URL or params mappings.
        requests.exceptions.RequestException: If there is an issue with the HTTP request.
    """
    headers = {
        "Accept": "application/json",
        "Authorization": api_key
    }
    account_name = load_from_dotenv(ACCOUNT_VARIABLE_NAME)
    sandbox_name = load_from_dotenv(SANDBOX_VARIABLE_NAME)
    url = build_url(account_name, sandbox_name, config, data_type)
    params = get_params(config, data_type)
    data = fetch_data(url, headers, params)
    data = process_data(data, data_type)
    return data

def export_to_csv(data, output_file):
    """
    Exports a DataFrame to CSV format.
    Args:
        data (pd.DataFrame): The DataFrame to export.
        output_file (str): The path to the CSV file.
    """
    if data is not None and not data.empty:
        data.to_csv(output_file, index=False)
        print(f"Les données ont été exportées avec succès vers {output_file}")
    else:
        print("Aucune donnée à exporter.")

def get_data_type_index():
    """
    Gets the desired data type from the user.
    
    Returns:
        str: The index of the chosen data type.
    """
    max_index = max([CONTRACTS_INDEX, DEPARTMENTS_INDEX, EMPLOYEES_INDEX, EXIT_INDEX])
    while True:
        print("Menu:")
        print(f"{CONTRACTS_INDEX}. Obtenir les contrats")
        print(f"{DEPARTMENTS_INDEX}. Obtenir les départments")
        print(f"{EMPLOYEES_INDEX}. Obtenir les employés")
        print(f"{EXIT_INDEX}. Quitter")
        choice = input(f"Choisissez une option ({EXIT_INDEX}-{max_index}) : ")
        
        if choice in [CONTRACTS_INDEX, DEPARTMENTS_INDEX, EMPLOYEES_INDEX]:
            return choice
        elif choice == EXIT_INDEX:
            print("Au revoir !")
            return choice
        else:
            print(f"Option invalide. Veuillez choisir un nombre entre {EXIT_INDEX} et {max_index}.")

def get_data_type(data_type_index):
    """
    Returns the data type string corresponding to the given index.
    Args:
        data_type_index (int): The index representing the data type.
    Returns:
        str: The data type string corresponding to the given index.
    """
    matching = {
        CONTRACTS_INDEX:'contracts',
        DEPARTMENTS_INDEX:'departments',
        EMPLOYEES_INDEX:'employees'
    }
    data_type = matching[data_type_index]
    return data_type

def main():
    """
    Main function to get data from the Lucca API and export it to a CSV file.
    """
    config = load_config(CONFIG_PATH)
    api_key = load_from_dotenv(API_KEY_VARIABLE_NAME)
    data_type_index = get_data_type_index()
    if data_type_index == EXIT_INDEX : 
        sys.exit(0)
    data_type = get_data_type(data_type_index)
    data = get_data(api_key, config, data_type)
    export_to_csv(data, f"{OUTPUT_DIR}{data_type}.csv")

if __name__ == "__main__":
    main()