import json
from typing import List, Dict, Any

def upload_data(filename: str) -> List[Dict[str, any]]:
       """
    Reads a JSON file and extracts the user records into a list.

    Parameters
    ----------
    filename : str
        The path to the JSON file to be read in the file system.

    Returns
    -------
    list of dict
       A list containing the user records with their associated data.
       """
       
       with open(filename, 'r', encoding='utf-8') as file_handler:
              users_list: List[Dict[str, Any]] = json.load(file_handler)
              return users_list

users_list = upload_data("receitas_sinteticas.json")