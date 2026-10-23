from sys import argv
def create_table(command,database):
    print("###################### CREATE #########################")
    parts = command.split(maxsplit=2)
    if len(parts) == 3:
        table_name = parts[1]
        columns = parts[2].split(",") #This code separates the given data and extracts the table name and column names.
        if table_name not in database:
            database[table_name] = {"columns": columns, "rows": []}
            print(f"Table '{table_name}' created with columns: {columns}")
    try:
        if len(parts) != 3:
            raise ValueError
    except ValueError:
        print("The CREATE command in the file is in an invalid format.")
        return
    print("#######################################################")
    print("")
    return database
def print_table(command,database):
    parts = command.split(maxsplit=1)
    table_name = parts[0]
    # To determine the selected columns; if no columns are provided, all columns are taken.
    selected_columns = (parts[1].split(",") if len(parts) > 1 else database[table_name]["columns"])
    print("")
    print(f"Table: {table_name}")
    column_widths = {col: len(col) for col in selected_columns} # Initially sets column widths based on the length of column names.
    for row in database[table_name]["rows"]:
        for i, cell in enumerate(row):
            col_name = database[table_name]["columns"][i]
            if col_name in selected_columns:
                # Updates the selected column width by taking the maximum of the cell length and the current width.
                column_widths[col_name] = max(column_widths[col_name], len(str(cell)))
    print("+" + "+".join([("-" * (column_widths[col] + 2)) for col in selected_columns]) + "+")
    header = "| " + " | ".join([f"{col:<{column_widths[col]}}" for col in selected_columns]) + " |"
    print(header)
    print("+" + "+".join([("-" * (column_widths[col] + 2)) for col in selected_columns]) + "+")
    for row in database[table_name]["rows"]:
        filtered_row = [str(row[database[table_name]["columns"].index(col)]) for col in selected_columns]
        print("| " + " | ".join([f"{str(cell):<{column_widths[selected_columns[i]]}}" for i, cell in enumerate(filtered_row)]) + " |")
    print("+" + "+".join([("-" * (column_widths[col] + 2)) for col in selected_columns]) + "+")
def insert_into_table(command,database):
    """This function processes the data read from the input file into the specified table,
    prints the table, and shows a meaningful error message if the table name is not found."""
    print("###################### INSERT #########################")
    parts = command.split(maxsplit=2)
    try:
        if len(parts) != 3:
            raise IndexError("Invalid command format.")
        table_name = parts[1]
        data = tuple(parts[2].split(","))
        if table_name not in database:
            raise KeyError
        table_columns = database[table_name]["columns"]
        if len(data) != len(table_columns):
            raise ValueError
        # Adds new data to the table
        database[table_name]["rows"].append(data)
        print(f"Inserted into '{table_name}': {data}")
        print_table(table_name,database)
    except IndexError:
        print("The INSERT command in the file is in an invalid format.")
    except KeyError :
        table_name = parts[1]
        data = tuple(parts[2].split(","))
        print(f"Table {table_name} not found")
        print(f"Inserted into '{table_name}': {data}")
    except ValueError :
        table_name = parts[1]
        data = tuple(parts[2].split(","))
        table_columns = database[table_name]["columns"]
        print(f"Column mismatch: Expected {len(table_columns)} values, but got {len(data)}.")
        print("The insert operation couldn't be completed.")
    finally:
       print("#######################################################")
       print("")
    return database
def select_from_table(command,database):
    print("###################### SELECT #########################")
    try:
        parts = command.split(maxsplit=2)
        try:
            if len(parts) < 3:
                raise ValueError
        except ValueError:
            print("The SELECT command in the file is in an invalid format.")
            return
        table_name = parts[1]
        columns_and_conditions = parts[2]
        try:
            if table_name not in database:
                raise KeyError
        except KeyError:
            conditions = columns_and_conditions.split("WHERE")[-1].strip()
            conditions = "{" + conditions + "}"  # adds curly braces to match the format
            # Convert each condition into key-value pairs, and clean them up.
            conditions = dict([tuple(condition.split(":")) for condition in conditions.strip("{}").split(",")])
            conditions = {key.strip().strip('"'): value.strip().strip('"') for key, value in conditions.items()}
            print(f"Table {table_name} not found")
            print(f"Condition: {conditions}")
            print(f"Select result from '{table_name}': None")
            return
        if "WHERE" in columns_and_conditions:
            columns, conditions = columns_and_conditions.split("WHERE")
            columns = columns.strip().split(",")
            conditions = conditions.strip()[1:-1]
            # Convert conditions into key-value pairs
            conditions = dict([tuple(condition.split(":")) for condition in conditions.split(",")])
            # Remove extra quotes and spaces from both keys and values
            conditions = {key.strip().strip('"'): value.strip().strip('"') for key, value in conditions.items()}
        else:
            columns = columns_and_conditions.strip().split(",")
            conditions = {}
        table_columns = database[table_name]["columns"]
        rows = database[table_name]["rows"]
        selected_rows = []
        if "*" in columns:  # For "SELECT <table_name> * WHERE"
            columns = table_columns
        for col in columns:
            try:
                if col.strip() not in table_columns:
                    raise KeyError
            except KeyError:
                print(f"Column {col.strip()} does not exist")
                print(f"Condition: {conditions}")
                print(f"Select result from '{table_name}': None")
                return
        for row in rows:
            # Check each row for matching conditions
            match = True
            for column_name, value in conditions.items():
                column_name = column_name.strip().strip('"')
                value = value.strip().strip('"')
                try:
                    if column_name not in table_columns:
                        raise KeyError
                except KeyError:
                    print(f"Column {column_name} does not exist")
                    print(f"Condition: {conditions}")
                    print(f"Select result from '{table_name}': None")
                    return
                col_index = table_columns.index(column_name)
                if str(row[col_index]).strip() != value.strip():
                    match = False
                    break
            if match:
                selected_row = tuple(row[table_columns.index(col.strip())] for col in columns)
                selected_rows.append(selected_row)
        print(f"Condition: {conditions}")
        print(f"Select result from '{table_name}': {selected_rows}")
    except Exception as e:
        print(f"Error: {str(e)}")
        return
    finally:
        print("#######################################################")
        print("")
    return database
def update_table(command,database):
    print("###################### UPDATE #########################")
    try:
        parts = command.split(maxsplit=2)
        try:
            if len(parts) < 3:
                raise ValueError
        except ValueError:
            print("The UPDATE command in the file is in an invalid format.")
            return
        table_name = parts[1]
        updates_and_conditions = parts[2]
        updates_str, conditions_str = updates_and_conditions.split("WHERE")
        # Remove {} characters from the condition and update sections.
        updates = updates_str.strip()[1:-1]
        conditions = conditions_str.strip()[1:-1]
        # Convert updates and conditions into dictionaries
        updates = dict([tuple(update.split(":")) for update in updates.split(",")])
        conditions = dict([tuple(condition.split(":")) for condition in conditions.split(",")])
        #To clean up extra spaces and quotes from the keys and values in the updates and conditions dictionaries.
        updates = {key.strip().strip('"'): value.strip().strip('"') for key, value in updates.items()}
        conditions = {key.strip().strip('"'): value.strip().strip('"') for key, value in conditions.items()}
        try:
            if table_name not in database:
                raise KeyError
        except KeyError:
            print(f"Updated '{table_name}' with {updates} where {conditions}")
            print(f"Table {table_name} not found")
            print(f"0 rows updated.")
            return
        rows = database[table_name]["rows"]
        updated_rows = 0
        for column_name in updates.keys():
            try:
                if column_name not in database[table_name]["columns"]:
                    raise KeyError
            except KeyError:
                print(f"Updated '{table_name}' with {updates} where {conditions}")
                print(f"Column {column_name} does not exist")
                print(f"0 rows updated.")
                print_table(table_name,database)
                return
        for i, row in enumerate(rows):
            if isinstance(row, tuple):
                row = list(row)  # Convert tuple to list to allow modifications
                rows[i] = row
            match = True
            for column_name, value in conditions.items():
                #to check columns based on conditions, error if the column is missing, and skip the row if the values don't match.
                try:
                    col_index = database[table_name]["columns"].index(column_name)
                except ValueError:
                    print(f"Updated '{table_name}' with {updates} where {conditions}")
                    print(f"Column {column_name} does not exist")
                    print(f"{updated_rows} rows updated.")
                    print_table(table_name,database)
                    return
                if str(row[col_index]).strip() != value.strip():
                    match = False
                    break
            if match:
                for column_name, new_value in updates.items():
                    col_index = database[table_name]["columns"].index(column_name)
                    row[col_index] = new_value  # Update with new values
                rows[i] = tuple(row)  # Convert back to tuple
                updated_rows += 1
        print(f"Updated '{table_name}' with {updates} where {conditions}")
        print(f"{updated_rows} rows updated.")
        print_table(table_name,database)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("#######################################################")
        print("")
    return database
def delete_from_table(command,database):
    print("###################### DELETE #########################")
    try:
        parts = command.split(maxsplit=2)
        try:
            if len(parts) < 2:
                raise ValueError
        except ValueError:
            print("The DELETE command in the file is in an invalid format.")
            return
        table_name = parts[1]
        if len(parts) == 2:
            try:
                if table_name not in database:
                    raise KeyError
            except KeyError:
                print(f"Deleted from '{table_name}' where ALL rows")
                print(f"Table {table_name} not found")
                print(f"0 rows deleted.")
                return
            # Deletes all rows if the table exists.
            deleted_rows = len(database[table_name]["rows"])
            database[table_name]["rows"] = []
            print(f"Deleted all rows from '{table_name}'.")
            print(f"{deleted_rows} rows deleted.")
            print_table(table_name,database)
            return
        # For taking the condition part, removing unnecessary characters
        conditions_str = parts[2]
        conditions_str = conditions_str.strip()[5:]  # Remove 'WHERE'
        conditions_str = conditions_str.strip()[1:-1]  # Remove curly braces
        # Replaces quotes to fit the format
        conditions_string = parts[2][6:].replace('"', "'")
        # For converting the conditions into key-value pairs
        conditions = dict([tuple(condition.split(":")) for condition in conditions_str.split(",")])
        # For stripping extra spaces and quotes around keys and values
        conditions = {key.strip().strip('"'): value.strip().strip('"') for key, value in conditions.items()}
        try:
            if table_name not in database:
                raise KeyError
        except KeyError:
            print(f"Deleted from '{table_name}' where {conditions_string}")
            print(f"Table {table_name} not found")
            print(f"0 rows deleted.")
            return
        rows = database[table_name]["rows"]
        deleted_rows = 0
        rows_to_delete = []
        for i, row in enumerate(rows):
            """This loop checks each row for matching conditions and adds the indices 
            of the matching rows to the rows_to_delete list. If a column is not found, 
            it writes an error message and stops the operation."""
            match = True
            for column_name, value in conditions.items():
                try:
                    col_index = database[table_name]["columns"].index(column_name)
                except ValueError:
                    print(f"Deleted from '{table_name}' where {conditions_string}")
                    print(f"Column {column_name} does not exist")
                    print(f"0 rows deleted.")
                    print_table(table_name,database)
                    return
                if str(row[col_index]).strip() != value.strip():
                    match = False
                    break
            if match:
                rows_to_delete.append(i)
        for i in sorted(rows_to_delete, reverse=True):
            """Rows are deleted in reverse order because deleting a row shifts the indices 
            of the remaining ones. By deleting from the end, we avoid confusion 
            caused by these index changes."""
            rows.pop(i)
            deleted_rows += 1
        print(f"Deleted from '{table_name}' where {conditions_string}")
        print(f"{deleted_rows} rows deleted.")
        print_table(table_name,database)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("#######################################################")
        print("")
    return database
def join_tables(command,database):
    print("####################### JOIN ##########################")
    try:
        parts = command.split(maxsplit=3)
        try:
            if len(parts) < 4 or parts[2] != "ON":
                raise ValueError
        except ValueError:
            print("The JOIN command in the file is invalid or the 'ON' statement is missing.")
            return
        table1, table2 = parts[1].split(",")
        column = parts[3]
        try:
            if table1 not in database:
                raise KeyError
        except KeyError:
            print(f"Join tables {table1} and {table2}")
            print(f"Table {table1} does not exist")
            return
        try:
            if table2 not in database:
                raise KeyError
        except KeyError:
            print(f"Join tables {table1} and {table2}")
            print(f"Table {table2} does not exist")
            return
        table1_columns = database[table1]["columns"]
        table2_columns = database[table2]["columns"]
        try:
            if column not in table1_columns or column not in table2_columns:
                raise KeyError
        except KeyError:
            print(f"Join tables {table1} and {table2}")
            print(f"Column {column} does not exist")
            return
        # For getting column indices from both tables and initializing join_result.
        table1_col_index = table1_columns.index(column)
        table2_col_index = table2_columns.index(column)
        join_result = []
        # For combining matching rows and adding them to join_result.
        for row1 in database[table1]["rows"]:
            for row2 in database[table2]["rows"]:
                if row1[table1_col_index] == row2[table2_col_index]:
                    join_result.append(tuple(row1) + tuple(row2))
        print(f"Join tables {table1} and {table2}")
        print(f"Join result ({len(join_result)} rows):")
        print("")
        # For preparing and displaying the joined table columns
        join_table_columns = table1_columns + table2_columns
        print(f"Table: Joined Table")
        print_table_from_rows(join_result, join_table_columns)
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("#######################################################")
        print("")
    return database
def print_table_from_rows(rows, columns):
    """This function prints a table with given rows and columns in the proper format"""
    column_widths = [len(columns[i]) for i in range(len(columns))]
    for row in rows:
        for i, cell in enumerate(row):
            column_widths[i] = max(column_widths[i], len(str(cell)))
    def create_separator():
        return "+" + "+".join(["-" * (width + 2) for width in column_widths]) + "+"
    def create_row(row):
        return "| " + " | ".join([f"{str(row[i]):<{column_widths[i]}}" for i in range(len(row))]) + " |"
    separator = create_separator()
    print(separator)
    header = "| " + " | ".join([f"{columns[i]:<{column_widths[i]}}" for i in range(len(columns))]) + " |"
    print(header)
    print(separator)
    for row in rows:
        print(create_row(row))
    print(separator)
def count_rows(command,database):
    print("###################### COUNT #########################")
    try:
        parts = command.split(maxsplit=3)
        try:
            if len(parts) < 3 or parts[0] != "COUNT":
                raise ValueError
        except ValueError:
            print("The COUNT command in the file is in an invalid format.")
            return
        table_name = parts[1]
        if len(parts) == 3 or (len(parts) > 3 and parts[2] == "WHERE" and parts[3] == "*"):
            """This if statement checks if the table exists and it counts the rows and writes the result 
            to the file if it exists. If not, it writes an error message."""
            try:
                if table_name not in database:
                    raise KeyError
            except KeyError:
                print(f"Table {table_name} not found")
                print(f"Total number of entries in '{table_name}' is 0")
                return
            total_count = len(database[table_name]["rows"])
            print(f"Count: {total_count}")
            print(f"Total number of entries in '{table_name}' is {total_count}")
            return
        # Parsing and processing the conditions
        conditions_str = parts[3].strip("{}")
        conditions_pairs = conditions_str.split(", ")
        conditions = {}
        for pair in conditions_pairs:
            """This loop splits condition pairs, removes quotes,
            and adds them to the conditions dictionary."""
            key, value = pair.split(": ")
            key = key.strip('"')
            value = value.strip('"')
            conditions[key] = value
        try:
            if table_name not in database:
                raise KeyError
        except KeyError:
            print(f"Table {table_name} not found")
            print(f"Total number of entries in '{table_name}' is 0")
            return
        table_columns = database[table_name]["columns"]
        table_rows = database[table_name]["rows"]
        count = 0
        for row in table_rows:
            """This loop checks each row for matching conditions and counts the rows that match.
            (Variable "match" is used to record the match)
            If a column is not found, it writes an error message and stops the operation."""
            match = True
            for condition_col, condition_val in conditions.items():
                try:
                    if condition_col not in table_columns:
                        raise KeyError
                except KeyError:
                    print(f"Column {condition_col} does not exist")
                    print(f"Total number of entries in '{table_name}' is 0")
                    return
                col_index = table_columns.index(condition_col)
                if str(row[col_index]).strip() != condition_val.strip():
                    match = False
                    break
            if match:
                count += 1
        print(f"Count: {count}")
        print(f"Total number of entries in '{table_name}' is {count}")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        print("#######################################################")
        print("")
    return database
def main():
    try:
        f_in = open(argv[1], "r")
    except IndexError:
        print("Please enter a file name.")
        exit()
    except FileNotFoundError:
        print(f"File '{argv[1]}' cannot be found. It is recommended to check the file path.")
        exit()
    database = {}
    for line in f_in:
        command = line.strip()
        if command.startswith("CREATE_TABLE"):
            create_table(command, database)
        elif command.startswith("INSERT"):
            insert_into_table(command, database)
        elif command.startswith("SELECT"):
            select_from_table(command, database)
        elif command.startswith("UPDATE"):
            update_table(command, database)
        elif command.startswith("DELETE"):
            delete_from_table(command, database)
        elif command.startswith("JOIN"):
            join_tables(command, database)
        elif command.startswith("COUNT"):
            count_rows(command, database)
    f_in.close()
if __name__ == "__main__":
    main()
