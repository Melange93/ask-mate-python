def write_table_to_file(file_name, table):
    with open(file_name, "w") as file:
        for record in table:
            row = ','.join(record)
            file.write(row + "\n")

def get_table_from_file(file_name):
    with open(file_name, "r") as file:
        lines = file.readlines()
    table = [element.replace("\n", "").split(",") for element in lines]
    return table