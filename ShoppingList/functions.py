FILEPATH = "ShoppingList/list.txt"


def get_list(filepath=FILEPATH):
    """ Read a text file and return a list
        of to-do items.
    """
    # promennou FILE jsem prejmenoval na file_local, je to kvuli prehlednosti kodu, promenna v funkci je vzdy jen LOKALNI !!
    # stejne tak pro TODOS na todos_local !!!
    with open(filepath, "r") as file_local:
        lists_local = file_local.readlines()
        return lists_local

def write_lists(lists_arg, filepath=FILEPATH):
    # podtimto je DOC String, da se zobrayit pomoci volani help(write_todos)
    """ Write the to-do items list in the text file."""
    with open(filepath, "w") as file_local:
        file_local.writelines(lists_arg)