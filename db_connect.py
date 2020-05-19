import pyodbc

# vars

db_name = "msdb"


server_name = "localhost"
username = ""
password = ""


# function returns "connection" object for MS SQL Server connect

def db_connect(server, database_name):
    connection = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database_name + ';' + 'UID=' + username + ';PWD=' + password + ';')

    return connection
