import json
import sys

# File to be analyzed
file_path = "C:\Scripts\Zabbix\MSSQLBackup Analizer\json_output.txt"

# Figure out if there is an argument passed to the script
try:
    # If it is, then we create a variable with the value of this argument
    passed_db = sys.argv[1]

except IndexError:
    # If it's not, then we just print out all the bases in LLD format

    # Starting of LLD format output print
    print("{\"data\":[")

    # Now we need to analyze file, line by line to extract desired data from it

    # First of all we need number of lines as it is equal to number of bases in question
    db_num = len(open(file_path).readlines())

    # Loop counter, so we know then to print the last line
    db_con_num = 1

    # Open the file in read mode
    with open(file_path, "r") as json_file:
        # Read first line
        line = json_file.readline()

        while line:
            # Parsing the line and making it JSON
            json_line = json.loads(line)

            # Print DB name. It depends on an order of elements. If the element is not the last, there will be
            # a comma in the end and in the end of the last element a curly bracket.
            if db_con_num == db_num:
                print("{\"{#MSSQL_DBNAME_}\":\"" + json_line.get('database') + "\"}]}")
            else:
                print("{\"{#MSSQL_DBNAME_}\":\"" + json_line.get('database') + "\"},")

            # Read next line
            line = json_file.readline()

            # Increse the loop counter
            db_con_num = db_con_num + 1

    # Close the file
    json_file.close()
    # Quit the program
    quit()

# If there is an argument passed to the script we compare it to databases names and if they are match we print
# backup status of this database.
with open(file_path, "r") as json_file:
    line = json_file.readline()

    while line:
        json_line = json.loads(line)

        if passed_db == json_line.get('database'):
            print(json_line.get('backup_status'))

        line = json_file.readline()

json_file.close()
quit()
