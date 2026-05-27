
from upload_data import upload_data, users_list

x = "290000000"
y = "300000000"

def filter_names_by_id(records: list[dict[str, int | str | list[str]]], condition) -> list[dict[str, int | str]]:
       """
    Filters user records based on a condition and extracts only the ID and name.

    Parameters
    ----------
    records : list[dict[str, int | str | list[str]]]
        A list of dictionaries representing the complete user records.
    condition : function
        A function that takes an ID (int) as an argument and returns a boolean.

    Returns
    -------
    list[dict[str, int | str]]
        A list of dictionaries containing strictly the 'id' (int) and 'nome' (str).
    """
     
       return ({'id': r['id'], 'nome': r['nome']} for r in records if condition(r["id"]))


def get_prescriptions(records: list[dict[str, int | str | list[str]]], condition) -> list[dict[str, int | str | list[str]]]:
       """
    Filters user records based on a condition and extracts the ID, name, and prescriptions.

    Parameters
    ----------
    records : list[dict[str, int | str | list[str]]]
        A list of dictionaries representing the complete user records.
    condition : function
        A function that takes an ID (int) as an argument and returns a boolean.

    Returns
    -------
    list[dict[str, int | str | list[str]]]
        A list of dictionaries containing strictly the 'id' (int), 'nome' (str), 
        and 'medicamentos' (list[str]).
    """

       return (
       {"id": r["id"], 
        "nome": r["nome"], 
        "medicamentos": r.get("medicamentos", [])} 
        for r in records if condition(r["id"]))

def main() -> None:
    """
    Main execution function of the script.

    Coordinates the filtering workflow by establishing the range condition,
    calling the transformation functions, and printing the formatted results
    to the console.
    """
    # Lambda function defining the ID filtering range
    interval_condition = lambda id_: int(x) <= int(id_) <= int(y)
    
    # Data processing using higher-order functions
    result_basic_info = filter_names_by_id(users_list, interval_condition)
    result_prescriptions = get_prescriptions(users_list, interval_condition)
       
    print("--- BASIC INFORMATION ---")
    for user in result_basic_info:
        print(user)

    print("\n--- PRESCRIPTIONS IN RANGE ---")
    for user in result_prescriptions:
        print(user)


if __name__ == '__main__':
    main()