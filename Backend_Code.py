import csv
# Example usage:
file_path = 'phone_book.csv'
def read_phone_book(filename):
    """
    Reads phone book records from a CSV file and returns a list of dictionaries.

    Args:
        filename: The path to the file.

    Returns:
        A list of dictionaries, where each dictionary represents a phone book record.
    """
    records = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            records.append(row)

    return records

import csv

def read_phone_book(filename):
    records = []

    with open(filename, 'r') as f:
        reader = csv.DictReader(f)
        next(reader, None)  # Skip the header row
        for row in reader:
            records.append(row)

    return records
def insert_into_phone_records(filename, values):
    new_record = {
        'id': values[0],
        'Name': values[1],
        'Email': values[2],
        'Phone_1': values[3],
        'Phone_2': values[4] if len(values) > 4 else None,
    }

    with open(filename, 'a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['id', 'Name', 'Email', 'Phone_1', 'Phone_2'])
        writer.writerow(new_record)

    return new_record

def execute_sql_command(command, filename):
    parts = command.split()

    if parts[0].upper() == "SELECT":
        if parts[1] == "*" and parts[2].upper() == "FROM" and parts[3].lower() == "phone_records" and len(parts) == 4:
            print(parts[0], parts[1], parts[2], parts[3])
            return read_phone_book(filename)
        elif len(parts) == 8 and parts[1] == "*" and parts[2].upper() == "FROM" and parts[4].upper() == "WHERE":
            filter_name = parts[6].strip("'")
            return [record for record in read_phone_book(filename) if record['Name'].lower() == filter_name.lower()]
    elif parts[0].upper() == "INSERT" and parts[1].upper() == "INTO":
        if parts[2].lower() == "phone_records" and parts[3].startswith("(") and parts[-1].endswith(")"):
            values = parts[4:-1]
            values = [value.strip("',") for value in values]
            return [insert_into_phone_records(filename, values)]
    elif parts[0].upper() == "DELETE" and parts[1].upper() == "FROM":
        if parts[2].lower() == "phone_records" and parts[3].upper() == "WHERE" and parts[5].lower() == "name" and len(parts) == 8:
            filter_name = parts[7].strip("'")
            existing_records = read_phone_book(filename)
            updated_records = [record for record in existing_records if record['Name'].lower() != filter_name.lower()]
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['id', 'Name', 'Email', 'Phone_1', 'Phone_2'])
                writer.writeheader()
                writer.writerows(updated_records)
            return updated_records

    #raise ValueError("Unsupported SQL command: " + command)

# 2.1 SELECT * FROM phone_records;
select_all_command = "SELECT * FROM phone_records"
result_select_all = execute_sql_command(select_all_command, file_path)
print("\n2.1 SELECT * FROM phone_records:")
for record in result_select_all:
    print(record)

# 2.2 SELECT * FROM phone_records WHERE name='Doe';
select_doe_command = "SELECT * FROM phone_records WHERE name='Doe'"
result_select_doe = execute_sql_command(select_doe_command, file_path)
print("\n2.2 SELECT * FROM phone_records WHERE name='Doe':")
for record in result_select_doe:
    print(record)

# 2.3 INSERT INTO phone_records(id, name, email, phone_1, phone_2) VALUES('11', 'Test', 'test@test.xtyz', '1234456', '1233233');
insert_command = "INSERT INTO phone_records(id, Name, Email, Phone_1, Phone_2) VALUES('12', 'Test', 'test@test.xtyz', '1234456', '1233233')"
result_insert = execute_sql_command(insert_command, file_path)
print("\n2.3 INSERT INTO phone_records(id, name, email, phone_1, phone_2):")
for record in result_insert:
    print(record)

# 2.4 DELETE FROM phone_records WHERE name='John';
delete_command = "DELETE FROM phone_records WHERE name='John'"
result_delete = execute_sql_command(delete_command, file_path)
print("\n2.4 DELETE FROM phone_records WHERE name='John':")
for record in result_delete:
    print(record)

# Display all records after operations
print("\nAll Records in the Dataset:")
all_records = read_phone_book(file_path)
for record in all_records:
    print(record)
